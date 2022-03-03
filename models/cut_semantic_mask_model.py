import numpy as np
import torch
from .cut_model import CUTModel
from . import networks
from .patchnce import PatchNCELoss
import util.util as util
from .modules import loss
import torch.nn.functional as F
from util.iter_calculator import IterCalculator
from util.network_group import NetworkGroup

class CUTSemanticMaskModel(CUTModel):
    """ This class implements CUT and FastCUT model, described in the paper
    Contrastive Learning for Unpaired Image-to-Image Translation
    Taesung Park, Alexei A. Efros, Richard Zhang, Jun-Yan Zhu
    ECCV, 2020

    The code borrows heavily from the PyTorch implementation of CycleGAN
    https://github.om/junyanz/pytorch-CycleGAN-and-pix2pix
    """
    @staticmethod
    def modify_commandline_options(parser, is_train=True):
        """  Configures options specific for CUT semantic mask model
        """
        parser = CUTModel.modify_commandline_options(parser, is_train=True)
        return parser
        
    def __init__(self, opt,rank):
        super().__init__(opt,rank)

        # specify the training losses you want to print out.
        # The training/test scripts will call <BaseModel.get_current_losses>
        losses_G = ['sem']
        if opt.train_mask_out_mask:
            losses_G += ['out_mask']

        losses_f_s = ['f_s']
        losses_f_t = ['f_t']

        self.loss_names_G += losses_G
        self.loss_names_f_s = losses_f_s
        self.loss_names_f_t = losses_f_t

        self.loss_names = self.loss_names_G + self.loss_names_D + self.loss_names_f_s + self.loss_names_f_t
            
        # define networks (both generator and discriminator)
        if self.isTrain:
            self.netf_s = networks.define_f(opt.model_input_nc, nclasses=opt.f_s_semantic_nclasses, 
                                            init_type=opt.model_init_type, init_gain=opt.model_init_gain,
                                            gpu_ids=self.gpu_ids, fs_light=opt.f_s_light)
            self.netf_t = networks.define_f(opt.model_input_nc, nclasses=opt.f_s_semantic_nclasses, 
                                            init_type=opt.model_init_type, init_gain=opt.model_init_gain,
                                            gpu_ids=self.gpu_ids, fs_light=opt.f_s_light)

            self.model_names += ['f_s']
            self.model_names += ['f_s', 'f_t']

            # define loss functions
            self.criterionf_s = torch.nn.modules.CrossEntropyLoss()
            self.criterionf_t = torch.nn.modules.CrossEntropyLoss()
            
            if opt.train_mask_out_mask:
                if opt.train_mask_loss_out_mask == 'L1':
                    self.criterionMask = torch.nn.L1Loss()
                elif opt.train_mask_loss_out_mask == 'MSE':
                    self.criterionMask = torch.nn.MSELoss()
                elif opt.train_mask_loss_out_mask == 'Charbonnier':
                    self.criterionMask = L1_Charbonnier_loss(opt.train_mask_charbonnier_eps)
           
            self.optimizer_f_s = torch.optim.Adam(self.netf_s.parameters(), lr=opt.train_sem_lr_f_s, betas=(opt.train_beta1, opt.train_beta2))
            self.optimizer_f_t = torch.optim.Adam(self.netf_t.parameters(), lr=opt.train_sem_lr_f_s, betas=(opt.train_beta1, opt.train_beta2))
            self.optimizers.append(self.optimizer_f_s)
            self.optimizers += [self.optimizer_f_s, self.optimizer_f_t]

            if self.opt.train_iter_size > 1 :
                self.iter_calculator = IterCalculator(self.loss_names)
                for i,cur_loss in enumerate(self.loss_names):
                    self.loss_names[i] = cur_loss + '_avg'
                    setattr(self, "loss_" + self.loss_names[i], 0)

            ###Making groups
            self.group_f_s = NetworkGroup(
                    networks_to_optimize=["f_s", "f_t"],
                    forward_functions=None,
                    backward_functions=["compute_f_s_loss", "compute_f_t_loss"],
                    loss_names_list=["loss_names_f_s","loss_names_f_t"],
                    optimizer=["optimizer_f_s","optimizer_f_t"],
                    loss_backward=["loss_f_s","loss_f_t"]
            )
            self.networks_groups.append(self.group_f_s)

            # add evaluator
            self.supervised_evaluators["segmentation"] = self.netf_t

    def set_input_first_gpu(self,data):
        super().set_input_first_gpu(data)
        self.input_A_label=self.input_A_label[:self.bs_per_gpu]
        if hasattr(self,'input_B_label'):
            self.input_B_label=self.input_B_label[:self.bs_per_gpu]
        
    def data_dependent_initialize(self, data):
        """
        The feature network netF is defined in terms of the shape of the intermediate, extracted
        features of the encoder portion of netG. Because of this, the weights of netF are
        initialized at the first feedforward pass with some input images.
        Please also see PatchSampleF.create_mlp(), which is called at the first forward() call.
        """
        super().data_dependent_initialize(data)
        visual_names_seg_A = ['input_A_label','gt_pred_A','pfB_max']

        if hasattr(self,'input_B_label'):
            visual_names_seg_B = ['input_B_label']
        else:
            visual_names_seg_B = []

        visual_names_seg_B += ['gt_pred_B']

        self.visual_names += [visual_names_seg_A,visual_names_seg_B]
        
        if self.opt.train_mask_out_mask and self.isTrain:
            visual_names_out_mask_A = ['real_A_out_mask','fake_B_out_mask']
            self.visual_names += [visual_names_out_mask_A]

        if self.opt.supervised_eval_fakes and self.isTrain:
            visual_names_eval_B = ['curr_real_B_val', 'curr_real_B_label_val', 'real_B_val_out_mask']
            self.visual_names += [visual_names_eval_B]
        
    def set_input(self, input):
        """Unpack input data from the dataloader and perform necessary pre-processing steps.
        Parameters:
            input (dict): include the data itself and its metadata information.
        The option 'direction' can be used to swap domain A and domain B.
        """
        super().set_input(input)
        if 'A_label' in input :
            self.input_A_label = input['A_label'].to(self.device).squeeze(1)
        if self.opt.train_mask_f_s_B and 'B_label' in input:
            self.input_B_label = input['B_label'].to(self.device).squeeze(1)

        
    def forward(self):
        """Run forward pass; called by both functions <optimize_parameters> and <test>."""
        super().forward()
        
        d = 1
        self.pred_real_A = self.netf_s(self.real_A)
        self.gt_pred_A = F.log_softmax(self.pred_real_A,dim= d).argmax(dim=d)

        self.pred_real_B = self.netf_s(self.real_B)
        self.gt_pred_B = F.log_softmax(self.pred_real_B,dim=d).argmax(dim=d)
            
        self.pred_fake_B = self.netf_s(self.fake_B)
        self.pfB = F.log_softmax(self.pred_fake_B,dim=d)#.argmax(dim=d)
        self.pfB_max = self.pfB.argmax(dim=d)

        if hasattr(self,'criterionMask'):
                label_A = self.input_A_label
                label_A_in = label_A.unsqueeze(1)
                label_A_inv = torch.tensor(np.ones(label_A.size())).to(self.device) - label_A>0.5
                label_A_inv = label_A_inv.unsqueeze(1)
                self.real_A_out_mask = self.real_A *label_A_inv
                self.fake_B_out_mask = self.fake_B *label_A_inv            
                
    def compute_G_loss(self):
        """Calculate GAN and NCE loss for the generator"""
        super().compute_G_loss()
        
        self.loss_sem = self.opt.train_sem_lambda * self.criterionf_s(self.pfB, self.input_A_label)
        if not hasattr(self, 'loss_f_s') or self.loss_f_s > self.opt.f_s_semantic_threshold:
            self.loss_sem = 0 * self.loss_sem
        self.loss_G += self.loss_sem

        if hasattr(self,'criterionMask'):
            self.loss_out_mask = self.criterionMask( self.real_A_out_mask, self.fake_B_out_mask) * self.opt.train_mask_lambda_out_mask
            self.loss_G += self.loss_out_mask

    def compute_f_s_loss(self):
        self.loss_f_s = 0
        if not self.opt.train_mask_no_train_f_s_A:
            label_A = self.input_A_label
            # forward only real source image through semantic classifier
            pred_A = self.netf_s(self.real_A) 
            self.loss_f_s += self.criterionf_s(pred_A, label_A)#.squeeze(1))
        if self.opt.train_mask_f_s_B:
            label_B = self.input_B_label
            pred_B = self.netf_s(self.real_B) 
            self.loss_f_s += self.criterionf_s(pred_B, label_B)#.squeeze(1))

    def compute_f_t_loss(self):
        self.loss_f_t = 0

        if self.opt.supervised_eval_fakes:
            label_fake_B = self.input_A_label
            pred_B = self.netf_t(self.fake_B.detach())
            self.loss_f_t += self.criterionf_t(pred_B, label_fake_B)
