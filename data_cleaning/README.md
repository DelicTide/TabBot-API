TabBot_version_2
2025-01-18-neo

*assuming image folder containg images of object wanted to train.

Step one: 

    pad.py:
        pad images for annotation (yolo_v11 640x640)

Step :

    create_batch.py
        put's desired training images into folders (batchs of 100 each) for annotation. 

Step two:

    annotate images: makesense.ai (manual human object labeling and bounding)

Step three:

    batch_2_data.py:
        takes annodated batch folders (i.e. data/images/batch_*, data/labels/batch_*) and creates a yolo training ./dir, data/images/(test/train/val), data/labels/(test/train/val).
        It also checks to verify if the image has a corresponding .txt. WARNING: images in this cleansing process without corresponding .txt files will be permanatley deleted. Please only proceed with annodated data when you are ready to donate your data to TabBot, forever.... hahaha....) 

TOOLs:

    revert.py
        takes the contents of two output folders (with_tabs, without_tabs) and puts them back in the parent directory. A good tool to re-run a model on the same image sets over and over for training and anslysis. 
