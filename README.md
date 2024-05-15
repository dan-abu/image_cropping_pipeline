**Overview**

The `main.py` script crops the `surgical_robot.jpeg` into three squares or rectangles of random sizes.
The script also gives the user the opportunity to resize the cropped images.
Once complete, the script displays the cropped images.
The requirements for running this script are included in the repo in `requirements.txt`.
I've also included the notebook I used for rough working under `scratch.ipynb`.
You will find the definition of the task that inspired this script below.

**Image transformer task**

For this task, you will be writing the first piece of an image transformation pipeline.
We would like you to write some code that allows us to randomly sample from an image.

**Requirements:**

• Given an image, your code should be able to return 3 random samples from the image.

• The 3 samples should not overlap. • A user should be able to configure the size of the samples to be generated.

• A user should receive meaningful errors if they provide arguments that are invalid.

• Your code should be written in such a way that other engineers could extend it to add additional transformations either before or after this sampling.
