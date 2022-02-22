# Load modules
import configparser


def get_several_input(config,sect,opt,f=False,i=False):
    var = config.get(sect,opt)
    var = var.replace(', ',',')
    var = var.split(',')
    if f:
        var = list(map(float,var))
    if i:
        var = list(map(int,var))
    return var

