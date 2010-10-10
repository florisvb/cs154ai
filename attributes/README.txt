The files in this folder contain attribute labels obtained from Mechanical
Turk workers on the Birds-200 dataset. The file labels.txt contains the actual
labels. Each line corresponds to one attribute label of the form: 
<image_id> <attribute_id> <is_present> <certainty_id> <worker_id>

The file 'images.txt' contains lines of the form: 
<image_id> <image_file_name>

The file 'images-dirs.txt' is the same as 'images.txt' but also includes the
directory names: 
<image_id> <full_image_path>

The file 'attributes.txt' contains lines of the form: 
<attribute_id> <attribute_name>

<is_present> is 0 or 1, and indicates whether or not the worker thought the
given attribute was present in the given image.

The file 'certainties.txt' contains lines of the form: 
<certainty_id> <certainty_name>

Each unique value of worker_id corresponds to a unique worker on Mechanical
Turk.

