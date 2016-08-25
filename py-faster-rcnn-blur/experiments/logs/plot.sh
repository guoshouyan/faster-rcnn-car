#!/bin/bash
echo $1
cat $1 | grep '#0: loss_bbox =' | cut -d' ' -f15 > loss_bbox
gnuplot -p -e "plot 'loss_bbox' with linespoints"
cat $1 | grep '#1: loss_cls =' | cut -d' ' -f15 > loss_cls
gnuplot -p -e "plot 'loss_cls' with linespoints"
cat $1 | grep '#2: rpn_cls_loss =' | cut -d' ' -f15 > rpn_cls_loss
gnuplot -p -e "plot 'rpn_cls_loss' with linespoints"
cat $1 | grep '#3: rpn_loss_bbox =' | cut -d' ' -f15 > rpn_loss_bbox
gnuplot -p -e "plot 'rpn_loss_bbox' with linespoints"
cat $1 | grep ', loss =' | cut -d' ' -f9 > loss
gnuplot -p -e "plot 'loss' with linespoints"
