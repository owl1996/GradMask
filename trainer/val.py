import torch

import utils
from imagenet import get_x_y_from_data_dict

def validate(val_loader, model, criterion, args, verbose=False):
    """
    Run evaluation
    """
    losses = utils.AverageMeter()
    top1 = utils.AverageMeter()

    # switch to evaluate mode
    model.eval()
    if torch.cuda.is_available():
        torch.cuda.set_device(int(args.gpu))
        device = torch.device(f"cuda:{int(args.gpu)}")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    if args.imagenet_arch:
        for i, data in enumerate(val_loader):
            image, target = get_x_y_from_data_dict(data, device)
            with torch.no_grad():
                output = model(image)
                loss = criterion(output, target)

            output = output.float()
            loss = loss.float()

            # measure accuracy and record loss
            prec1 = utils.accuracy(output.data, target)[0]
            losses.update(loss.item(), image.size(0))
            top1.update(prec1.item(), image.size(0))

            if i % args.print_freq == 0:
                print(
                    "Test: [{0}/{1}]\t"
                    "Loss {loss.val:.4f} ({loss.avg:.4f})\t"
                    "Accuracy {top1.val:.3f} ({top1.avg:.3f})".format(
                        i, len(val_loader), loss=losses, top1=top1
                    )
                )
        if verbose:
            print("valid_accuracy {top1.avg:.3f}".format(top1=top1))    
    else:
        for i, (image, target) in enumerate(val_loader):
            image = image.to(device)
            target = target.to(device)

            # compute output
            with torch.no_grad():
                output = model(image)
                loss = criterion(output, target)

            output = output.float()
            loss = loss.float()

            # measure accuracy and record loss
            prec1 = utils.accuracy(output.data, target)[0]
            losses.update(loss.item(), image.size(0))
            top1.update(prec1.item(), image.size(0))

            if i % args.print_freq == 0 and verbose:
                print(
                    "Test: [{0}/{1}]\t"
                    "Loss {loss.val:.4f} ({loss.avg:.4f})\t"
                    "Accuracy {top1.val:.3f} ({top1.avg:.3f})".format(
                        i, len(val_loader), loss=losses, top1=top1
                    )
                )
        if verbose:
            print("valid_accuracy {top1.avg:.3f}".format(top1=top1))

    return top1.avg