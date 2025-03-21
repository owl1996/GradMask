import sys
import time
import torch
import utils
from .impl import iterative_unlearn

sys.path.append(".")
from imagenet import get_x_y_from_data_dict

@iterative_unlearn
def nothing(data_loaders, model, criterion, optimizer, epoch, args):
    forget_loader = data_loaders["forget"]
    retain_loader = data_loaders["retain"]
    retain_loader_iter = enumerate(retain_loader)

    losses = utils.AverageMeter()
    top1 = utils.AverageMeter()

    if torch.cuda.is_available():
        torch.cuda.set_device(int(args.gpu))
        device = torch.device(f"cuda:{int(args.gpu)}")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    start = time.time()    
    if args.imagenet_arch:
        for i, data in enumerate(forget_loader):
            # compute loss and grad on the retain
            _, data = next(retain_loader_iter)
            image, target = get_x_y_from_data_dict(data, device)
            output_clean = model(image)

            loss = criterion(output_clean, target)
            
            # measure accuracy and record loss
            output = output_clean.float()
            loss = loss.float()
            prec1 = utils.accuracy(output.data, target)[0]
            losses.update(loss.item(), image.size(0))
            top1.update(prec1.item(), image.size(0))

            if (i + 1) % args.print_freq == 0:
                end = time.time()
                print(
                    "Epoch: [{0}][{1}/{2}]\t"
                    "Loss {loss.val:.4f} ({loss.avg:.4f})\t"
                    "Accuracy {top1.val:.3f} ({top1.avg:.3f})\t"
                    "Time {3:.2f}".format(
                        epoch, i, len(forget_loader), end - start, loss=losses, top1=top1
                    )
                )
                start = time.time()
    else:
        for i, (image, target) in enumerate(forget_loader):
            # compute loss and grad on the retain
            _, data = next(retain_loader_iter)
            image, target = data[0].to(device), data[1].to(device)
            output_clean = model(image)

            loss = criterion(output_clean, target)

            # measure accuracy and record loss
            output = output_clean.float()
            loss = loss.float()
            prec1 = utils.accuracy(output.data, target)[0]
            losses.update(loss.item(), image.size(0))
            top1.update(prec1.item(), image.size(0))

            if (i + 1) % args.print_freq == 0:
                end = time.time()
                print(
                    "Epoch: [{0}][{1}/{2}]\t"
                    "Loss {loss.val:.4f} ({loss.avg:.4f})\t"
                    "Accuracy {top1.val:.3f} ({top1.avg:.3f})\t"
                    "Time {3:.2f}".format(
                        epoch, i, len(forget_loader), end - start, loss=losses, top1=top1
                    )
                )
                start = time.time()

    print("train_accuracy {top1.avg:.3f}".format(top1=top1))

    return top1.avg