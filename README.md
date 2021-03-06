# docmarker
A marker tool for making timed notes (for audio or video recordings or for live events/performances)
Intended usage is to create a list of time points in the recording/documentation of a performance or other event. 
We call the time points markers, and each marker may have additional info associated with it. 
Even if no additional info is entered, the list of time points can aid in recollecting which part of the performance contain notable events. 
Eentering additional info may help in differentiating the noted markers.

To run:
python doc_marker.py

Usage
* Enter markers with Alt+N (on Windows, use Command+N on OSX), where N is a number from 0 to 9
The marker will be set to the current time minus N, this allows you to drop markers for events that occured a few seconds into the past
Markers will have the following contents:
- time: current time
- synctime: optional time tag, for example set this to the playing time in the video or event being reviewed
- significance: the significance of the event (number from 0 to 9). Loosely differentiate between more and less important comments
- comment: free text comment describing what the marker
* When entering a new marker, the comment field will be automatically focused for convenience.
* Setting the sync time can be done by clicking in the sync time field. It will turn red when editing. Press enter to activate the changes.
* Starting or pausing the sync time can be done with the pushbutton "Sync:stopped/running". 
If you are reviewing a recorded performance and you need to stop to take more elaborate notes, it might be practical to stop the synctime while doing so.
* Setting significance for the last event can be done by pressing Alt+a (acuteness), then enter a number.
* Entering a comment for the last event can be done by pressing Alt+d (description), then typing in the comment
* All fields can also be updated in usual text editing manner by clicking on the field and typing in text
* When closing the window (exiting the program), the markers will be written to file. (DO TAKE CARE TO CLOSE WINDOW TO EXIT, or you will lose your markers)
* Saving can also be done at any time, using Alt+s

Merging marker lists from different sessions:
python merge_markerlists list1 list2 sort_by
Where sort_by can be 'time' or 'synctime'
This will create a new marker list with the name of list1 + '_merged'
