# Human-identification-Image-sequnces
Identifying Human objects from set of frames using frame differencing, connecting components, thresholding, and bounding boxes.  
## Test File
Juptyer Notebook - test.ipynb

## Code Structure
### find_bounding_box :
This function uses frame differencing, thresholding, connecting components and bounding boxes to create a bounding box around the human object
### person_present :
This function checks if a person is present in the frame or not.
### person_speed :
This function calculates the speed of the person and returns 2D numpy array.
## Running Instructions
import assignment1.py as ap
ap.FUNCTION_NAME(ARGUMENTS)

### OR
juptyer test.ipynb

## Example
![alt text](http://vlm1.uta.edu/~athitsos/courses/cse4310_spring2019/assignments/assignment1/bbox0062.jpg)
