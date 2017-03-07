#!/bin/sh

py_script_route="$HOME/Projects/yuv-tools"
files_route="$HOME/Projects/yuv-tools"
orig_ext="y4m"
enc_ext="mlhe"
options_mlhe="-pix_fmt yuv420p -ql 50"
options_mjpeg="-pix_fmt yuv420p -q:v 3"
options=$options_mlhe

if [ -f "$files_route/$1.$orig_ext" ]; then
	eval $(ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width "$files_route/$1.y4m")
	width=${streams_stream_0_width}
	height=${streams_stream_0_height}
else
	echo 'No existe el fichero!'
fi


echo -n 'Borrando archivos. '

if [ -f "$files_route/$1_orig.yuv" ]; then
	rm "$files_route/$1_orig.yuv"
fi

if [ -f "$files_route/$1_$enc_ext.yuv" ]; then
	rm "$files_route/$1_$enc_ext.yuv"
fi

if [ -f "$files_route/$1.$enc_ext" ]; then
	rm "$files_route/$1.$enc_ext"
fi


echo -n 'Generando '$1'_orig.yuv, '
ffmpeg -i "$files_route/$1.$orig_ext" -f rawvideo -vcodec rawvideo -pix_fmt nv12 "$files_route/$1_orig.yuv" > /dev/null 2>&1
echo -n $1'.'$enc_ext', '
ffmpeg -i "$files_route/$1.$orig_ext" $options "$files_route/$1.$enc_ext" > /dev/null 2>&1
echo $1'_lhe.yuv'
ffmpeg -i "$files_route/$1.$enc_ext" -f rawvideo -vcodec rawvideo -pix_fmt nv12 "$files_route/$1_$enc_ext.yuv" > /dev/null 2>&1

python "$py_script_route/psnr.py" "$files_route/$1_orig.yuv" $width $height NV12 "$files_route/$1_$enc_ext.yuv"
