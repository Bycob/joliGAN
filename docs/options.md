
# JoliGAN Options

Here are all the available options to call with `train.py`

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --checkpoints_dir | string | ./checkpoints | models are saved here |
| --dataroot | string | None | path to images (should have subfolders trainA, trainB, valA, valB, etc) |
| --ddp_port | string | 12355 |  |
| --gpu_ids | string | 0 | gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU |
| --madgrad | flag |  | if true madgrad optim will be used |
| --name | string | experiment_name | name of the experiment. It decides where to store samples and models |
| --phase | string | train | train, val, test, etc |
| --suffix | string |  | customized suffix: opt.name = opt.name + suffix: e.g., {model}_{netG}_size{load_size} |

## Discriminator

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --D_dropout | flag |  | whether to use dropout in the discriminator |
| --D_n_layers | int | 3 | only used if netD==n_layers |
| --D_ndf | int | 64 | \# of discrim filters in the first conv layer |
| --D_netD | string | basic | specify discriminator architecture, D_n_layers allows you to specify the layers in the discriminator<br/><br/>_**Values:** basic, n_layers, pixel, stylegan2, patchstylegan2, smallpatchstylegan2, projected_d, alexnet, vgg11, vgg11_bn, vgg13, vgg13_bn, vgg16, vgg16_bn, vgg19, vgg19_bn, resnet18, resnet34, resnet50, resnet101, resnet152, squeezenet1_0, squeezenet1_1, densenet121, densenet169, densenet161, densenet201, inception_v3, googlenet, shufflenet_v2_x0_5, shufflenet_v2_x1_0, shufflenet_v2_x1_5, shufflenet_v2_x2_0, mobilenet_v2, resnext50_32x4d, resnext101_32x8d, wide_resnet50_2, wide_resnet101_2, mnasnet0_75, mnasnet1_0, mnasnet1_3_ |
| --D_netD_global | string | none | specify discriminator architecture, any torchvision model can be used. By default no global discriminator will be used.<br/><br/>_**Values:** none, basic, n_layers, pixel, stylegan2, patchstylegan2, smallpatchstylegan2, projected_d, alexnet, vgg11, vgg11_bn, vgg13, vgg13_bn, vgg16, vgg16_bn, vgg19, vgg19_bn, resnet18, resnet34, resnet50, resnet101, resnet152, squeezenet1_0, squeezenet1_1, densenet121, densenet169, densenet161, densenet201, inception_v3, googlenet, shufflenet_v2_x0_5, shufflenet_v2_x1_0, shufflenet_v2_x1_5, shufflenet_v2_x2_0, mobilenet_v2, resnext50_32x4d, resnext101_32x8d, wide_resnet50_2, wide_resnet101_2, mnasnet0_75, mnasnet1_0, mnasnet1_3_ |
| --D_no_antialias | flag |  | if specified, use stride=2 convs instead of antialiased-downsampling (sad) |
| --D_no_antialias_up | flag |  | if specified, use [upconv(learned filter)] instead of [upconv(hard-coded [1,3,3,1] filter), conv] |
| --D_norm | string | instance | instance normalization or batch normalization for D<br/><br/>_**Values:** instance, batch, none_ |
| --D_proj_config_segformer | string | models/configs/segformer/segformer_config_b0.py | path to segformer configuration file |
| --D_proj_interp | int | -1 | whether to force projected discriminator interpolation to a value \> 224, -1 means no interpolation |
| --D_proj_network_type | string | efficientnet | <br/><br/>_**Values:** efficientnet, segformer, vitbase, vitsmall, vitsmall2_ |
| --D_proj_weight_segformer | string | models/configs/segformer/pretrain/segformer_mit-b0.pth | path to segformer weight |
| --D_spectral | flag |  | whether to use spectral norm in the discriminator |

## Generator

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --G_attn_nb_mask_attn | int | 10 |  |
| --G_attn_nb_mask_input | int | 1 |  |
| --G_config_segformer | string | models/configs/segformer/segformer_config_b0.py | path to segforme configuration file for G |
| --G_dropout | flag |  | dropout for the generator |
| --G_netG | string | mobile_resnet_attn | specify generator architecture<br/><br/>_**Values:** resnet_9blocks, resnet_6blocks, resnet_3blocks, resnet_12blocksmobile_resnet_9blocks, mobile_resnet_3blocksresnet_attn, mobile_resnet_attn, unet_256, unet_128, stylegan2, smallstylegan2, segformer_attn_conv, segformer_conv_ |
| --G_ngf | int | 64 | \# of gen filters in the last conv layer |
| --G_norm | string | instance | instance normalization or batch normalization for G<br/><br/>_**Values:** instance, batch, none_ |
| --G_padding_type | string | reflect | whether to use padding in the generator<br/><br/>_**Values:** reflect, replicate, zero_ |
| --G_spectral | flag |  | whether to use spectral norm in the generator |
| --G_stylegan2_num_downsampling | int | 1 | Number of downsampling layers used by StyleGAN2Generator |

## Algorithm-specific


### CUT model

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --alg_cut_flip_equivariance | flag |  | Enforce flip-equivariance as additional regularization. It's used by FastCUT, but not CUT |
| --alg_cut_lambda_GAN | float | 1.0 | weight for GAN loss：GAN(G(X)) |
| --alg_cut_lambda_NCE | float | 1.0 | weight for NCE loss: NCE(G(X), X) |
| --alg_cut_nce_T | float | 0.07 | temperature for NCE loss |
| --alg_cut_nce_idt | flag |  | use NCE loss for identity mapping: NCE(G(Y), Y)) |
| --alg_cut_nce_includes_all_negatives_from_minibatch | flag |  | (used for single image translation) If True, include the negatives from the other samples of the minibatch when computing the contrastive loss. Please see models/patchnce.py for more details. |
| --alg_cut_nce_layers | string | 0,4,8,12,16 | compute NCE loss on which layers |
| --alg_cut_netF | string | mlp_sample | how to downsample the feature map<br/><br/>_**Values:** sample, mlp_sample_ |
| --alg_cut_netF_dropout | flag |  | whether to use dropout with F |
| --alg_cut_netF_nc | int | 256 |  |
| --alg_cut_netF_norm | string | instance | instance normalization or batch normalization for F<br/><br/>_**Values:** instance, batch, none_ |
| --alg_cut_num_patches | int | 256 | number of patches per layer |

### CycleGAN model

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --alg_cyclegan_lambda_A | float | 10.0 | weight for cycle loss (A -\> B -\> A) |
| --alg_cyclegan_lambda_B | float | 10.0 | weight for cycle loss (B -\> A -\> B) |
| --alg_cyclegan_lambda_identity | float | 0.5 | use identity mapping. Setting lambda_identity other than 0 has an effect of scaling the weight of the identity mapping loss. For example, if the weight of the identity loss should be 10 times smaller than the weight of the reconstruction loss, please set lambda_identity = 0.1 |
| --alg_cyclegan_rec_noise | float | 0.0 | whether to add noise to reconstruction |

### ReCUT / ReCycleGAN

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --alg_re_P_lr | float | 0.0002 | initial learning rate for P networks |
| --alg_re_adversarial_loss_p | flag |  | if True, also train the prediction model with an adversarial loss |
| --alg_re_netP | string | unet_128 | specify P architecture<br/><br/>_**Values:** resnet_9blocks, resnet_6blocks, resnet_attn, unet_256, unet_128_ |
| --alg_re_no_train_P_fake_images | flag |  | if True, P wont be trained over fake images projections |
| --alg_re_nuplet_size | int | 3 | Number of frames loaded |
| --alg_re_projection_threshold | float | 1.0 | threshold of the real images projection loss below with fake projection and fake reconstruction losses are applied |

## Datasets

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --data_crop_size | int | 256 | then crop to this size |
| --data_dataset_mode | string | unaligned | chooses how datasets are loaded.<br/><br/>_**Values:** unaligned, unaligned_labeled, unaligned_labeled_mask, unaligned_labeled_mask_online_ |
| --data_direction | string | AtoB | AtoB or BtoA<br/><br/>_**Values:** AtoB, BtoA_ |
| --data_load_size | int | 286 | scale images to this size |
| --data_max_dataset_size | int | 1000000000 | Maximum number of samples allowed per dataset. If the dataset directory contains more than max_dataset_size, only a subset is loaded. |
| --data_num_threads | int | 4 | \# threads for loading data |
| --data_preprocess | string | resize_and_crop | scaling and cropping of images at load time<br/><br/>_**Values:** resize_and_crop, crop, scale_width, scale_width_and_crop, none_ |
| --data_relative_paths | flag |  | whether paths to images are relative to dataroot |
| --data_sanitize_paths | flag |  | if true, wrong images or labels paths will be removed before training |
| --data_serial_batches | flag |  | if true, takes images in order to make batches, otherwise takes them randomly |

### Online created datasets

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --data_online_creation_crop_delta_A | int | 50 | size of crops are random, values allowed are online_creation_crop_size more or less online_creation_crop_delta for domain A |
| --data_online_creation_crop_delta_B | int | 50 | size of crops are random, values allowed are online_creation_crop_size more or less online_creation_crop_delta for domain B |
| --data_online_creation_crop_size_A | int | 512 | crop to this size during online creation, it needs to be greater than bbox size for domain A |
| --data_online_creation_crop_size_B | int | 512 | crop to this size during online creation, it needs to be greater than bbox size for domain B |
| --data_online_creation_mask_delta_A | int | 0 | mask offset to allow genaration of a bigger object in domain B (for semantic loss) for domain A |
| --data_online_creation_mask_delta_B | int | 0 | mask offset to allow genaration of a bigger object in domain B (for semantic loss) for domain B |
| --data_online_creation_mask_square_A | flag |  | whether masks should be squared for domain A |
| --data_online_creation_mask_square_B | flag |  | whether masks should be squared for domain B |

## Semantic network

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --f_s_all_classes_as_one | flag |  | if true, all classes will be considered as the same one (ie foreground vs background) |
| --f_s_config_segformer | string | models/configs/segformer/segformer_config_b0.py | path to segformer configuration file for f_s |
| --f_s_dropout | flag |  | dropout for the semantic network |
| --f_s_net | string | vgg | specify f_s network [vgg|unet|segformer]<br/><br/>_**Values:** vgg, unet, segformer_ |
| --f_s_nf | int | 64 | \# of filters in the first conv layer of classifier |
| --f_s_semantic_nclasses | int | 2 | number of classes of the semantic loss classifier |
| --f_s_semantic_threshold | float | 1.0 | threshold of the semantic classifier loss below with semantic loss is applied |
| --f_s_weight_segformer | string | models/configs/segformer/pretrain/segformer_mit-b0.pth | path to segformer weight for f_s |

## Output

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --output_no_html | flag |  | do not save intermediate training results to [opt.checkpoints_dir]/[opt.name]/web/ |
| --output_print_freq | int | 100 | frequency of showing training results on console |
| --output_update_html_freq | int | 1000 | frequency of saving training results to html |
| --output_verbose | flag |  | if specified, print more debugging information |

### Visdom display

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --output_display_G_attention_masks | flag |  |  |
| --output_display_diff_fake_real | flag |  | if True x - G(x) is displayed |
| --output_display_env | string | main | visdom display environment name (default is "main") |
| --output_display_freq | int | 400 | frequency of showing training results on screen |
| --output_display_id | int | 1 | window id of the web display |
| --output_display_ncols | int | 4 | if positive, display all images in a single visdom web panel with certain number of images per row. |
| --output_display_networks | flag |  | Set True if you want to display networks on port 8000 |
| --output_display_port | int | 8097 | visdom port of the web display |
| --output_display_server | string | http://localhost | visdom server of the web display |
| --output_display_winsize | int | 256 | display window size for both visdom and HTML |

## Model parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --model_init_gain | float | 0.02 | scaling factor for normal, xavier and orthogonal. |
| --model_init_type | string | normal | network initialization<br/><br/>_**Values:** normal, xavier, kaiming, orthogonal_ |
| --model_input_nc | int | 3 | \# of input image channels: 3 for RGB and 1 for grayscale<br/><br/>_**Values:** 1, 3_ |
| --model_output_nc | int | 3 | \# of output image channels: 3 for RGB and 1 for grayscale<br/><br/>_**Values:** 1, 3_ |
| --model_type | string | cut | chooses which model to use.<br/><br/>_**Values:** cycle_gan, cut, cycle_gan_semantic, cut_semantic, cycle_gan_semantic_mask, cut_semantic_mask_ |

## Parameters used during training

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --train_D_accuracy_every | int | 1000 |  |
| --train_D_lr | float | 0.0002 | discriminator separate learning rate |
| --train_G_ema | flag |  | whether to build G via exponential moving average |
| --train_G_ema_beta | float | 0.999 | exponential decay for ema |
| --train_G_lr | float | 0.0002 | initial learning rate for generator |
| --train_batch_size | int | 1 | input batch size |
| --train_beta1 | float | 0.5 | momentum term of adam |
| --train_beta2 | float | 0.999 | momentum term of adam |
| --train_compute_D_accuracy | flag |  |  |
| --train_compute_fid | flag |  |  |
| --train_compute_fid_val | flag |  |  |
| --train_continue | flag |  | continue training: load the latest model |
| --train_epoch | string | latest | which epoch to load? set to latest to use latest cached model |
| --train_epoch_count | int | 1 | the starting epoch count, we save the model by \<epoch_count\>, \<epoch_count\>+\<save_latest_freq\>, ... |
| --train_fid_every | int | 1000 |  |
| --train_gan_mode | string | lsgan | the type of GAN objective. vanilla GAN loss is the cross-entropy objective used in the original GAN paper.<br/><br/>_**Values:** vanilla, lsgan, wgangp, projected_ |
| --train_iter_size | int | 1 | backward will be apllied each iter_size iterations, it simulate a greater batch size : its value is batch_size\*iter_size |
| --train_load_iter | int | 0 | which iteration to load? if load_iter \> 0, the code will load models by iter_[load_iter]; otherwise, the code will load models by [epoch] |
| --train_lr_decay_iters | int | 50 | multiply by a gamma every lr_decay_iters iterations |
| --train_lr_policy | string | linear | learning rate policy.<br/><br/>_**Values:** linear, step, plateau, cosine_ |
| --train_n_epochs | int | 100 | number of epochs with the initial learning rate |
| --train_n_epochs_decay | int | 100 | number of epochs to linearly decay learning rate to zero |
| --train_nb_img_max_fid | int | 1000000000 | Maximum number of samples allowed per dataset to compute fid. If the dataset directory contains more than nb_img_max_fid, only a subset is used. |
| --train_pool_size | int | 50 | the size of image buffer that stores previously generated images |
| --train_save_by_iter | flag |  | whether saves model by iteration |
| --train_save_epoch_freq | int | 5 | frequency of saving checkpoints at the end of epochs |
| --train_save_latest_freq | int | 5000 | frequency of saving the latest results |
| --train_use_contrastive_loss_D | flag |  |  |

### semantic training parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --train_sem_cls_B | flag |  | if true cls will be trained not only on domain A but also on domain B |
| --train_sem_cls_pretrained | flag |  | whether to use a pretrained model, available for non "basic" model only |
| --train_sem_cls_template | string | basic | classifier/regressor model type, from torchvision (resnet18, ...), default is custom simple model |
| --train_sem_l1_regression | flag |  | if true l1 loss will be used to compute regressor loss |
| --train_sem_lambda | float | 1.0 | weight for semantic loss |
| --train_sem_lr_f_s | float | 0.0002 | f_s learning rate |
| --train_sem_regression | flag |  | if true cls will be a regressor and not a classifier |
| --train_sem_use_label_B | flag |  | if true domain B has labels too |

### Parameters for semantic training with masks

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --train_mask_charbonnier_eps | float | 1e-06 | Charbonnier loss epsilon value |
| --train_mask_disjoint_f_s | flag |  | whether to use a disjoint f_s with the same exact structure |
| --train_mask_f_s_B | flag |  | if true f_s will be trained not only on domain A but also on domain B |
| --train_mask_for_removal | flag |  | if true, object removal mode, domain B images with label 0, cut models only |
| --train_mask_lambda_out_mask | float | 10.0 | weight for loss out mask |
| --train_mask_loss_out_mask | string | L1 | loss for out mask content (which should not change).<br/><br/>_**Values:** L1, MSE, Charbonnier_ |
| --train_mask_no_train_f_s_A | flag |  | if true f_s wont be trained on domain A |
| --train_mask_out_mask | flag |  | use loss out mask |

## Data augmentation

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| --dataaug_APA | flag |  | if true, G will be used as augmentation during D training adaptively to D overfitting between real and fake images |
| --dataaug_APA_every | int | 4 | How often to perform APA adjustment? |
| --dataaug_APA_nimg | int | 50 | APA adjustment speed, measured in how many images it takes for p to increase/decrease by one unit. |
| --dataaug_APA_p | int | 0 | initial value of probability APA |
| --dataaug_APA_target | float | 0.6 |  |
| --dataaug_D_label_smooth | flag |  | whether to use one-sided label smoothing with discriminator |
| --dataaug_D_noise | float | 0.0 | whether to add instance noise to discriminator inputs |
| --dataaug_affine | float | 0.0 | if specified, apply random affine transforms to the images for data augmentation |
| --dataaug_affine_scale_max | float | 1.2 | if random affine specified, max scale range value |
| --dataaug_affine_scale_min | float | 0.8 | if random affine specified, min scale range value |
| --dataaug_affine_shear | int | 45 | if random affine specified, shear range (0,value) |
| --dataaug_affine_translate | float | 0.2 | if random affine specified, translation range (-value\*img_size,+value\*img_size) value |
| --dataaug_diff_aug_policy | string |  | choose the augmentation policy : color randaffine. If you want more than one, please write them separated by a comma with no space (e.g. color,randaffine) |
| --dataaug_diff_aug_proba | float | 0.5 | proba of using each transformation |
| --dataaug_imgaug | flag |  | whether to apply random image augmentation |
| --dataaug_no_flip | flag |  | if specified, do not flip the images for data augmentation |
| --dataaug_no_rotate | flag |  | if specified, do not rotate the images for data augmentation |

