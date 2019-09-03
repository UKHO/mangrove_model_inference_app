from keras import backend as K


def sorensen_dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    coef = (2. * intersection + K.epsilon()) / (K.sum(y_true_f) + K.sum(y_pred_f) + K.epsilon())
    return coef


def sorensen_dice_coef_loss(y_true, y_pred):
    return 1 - sorensen_dice_coef(y_true, y_pred)
