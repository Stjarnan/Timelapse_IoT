# Timelapse_IoT
 Repeatedly capture photos on IoT devices to create a timelapse

 * Perhaps you would like to capture the process of blooming flowers?

# USAGE

Run the following commands in your terminal:

## To capture photos
```
python capture_timelapse_frames.py --output outputpath  --delay delayinseconds --display (1 or 0 depending on if you want to display capture photos on-screen)

```

## To create a timelapse video
```
python timelapse_process_images.py --input pathtoimages --output pathtooutputvideo	--fps 30

``` 