from psychopy import visual, core

from image_container import ImageContainer
from task import Task

mywin = visual.Window([1000,800], monitor="testMonitor", units="deg", color="white")
container = ImageContainer(mywin) # load images

print(f"monitor refresh rate: {1/mywin.monitorFramePeriod} Hz")

container.loading.draw()
mywin.flip()

task = Task(container)
task.run()
task.process_data()
task.save_data()

mywin.close()
core.quit()