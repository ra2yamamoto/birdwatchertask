from psychopy import visual, core, event
import atexit

from image_container import ImageContainer
from task import Task

mywin = visual.Window([1000,800], monitor="testMonitor", units="deg", color="white")
container = ImageContainer(mywin) # load images

print(f"monitor refresh rate: {1/mywin.monitorFramePeriod} Hz")

container.loading.draw()
mywin.flip()

task = Task(container)

atexit.register(task.save_data) # register exit procedure to process + store data in case experiment terminated early
atexit.register(task.process_data)

task.run()

mywin.close()
core.quit()