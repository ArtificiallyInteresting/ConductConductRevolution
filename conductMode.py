

import cv2
from util import *
import vision
import audio
import time

class conductMode:
    def __init__(self, trackname):
        self.startTime = time.time()
        self.bpm = 113 #todo this should come from the track file.
        self.secondsPerBeat = (60.0/self.bpm)
        self.beatsDone = 0
        self.notes = []
        self.score = 0
        with open(trackname + ".txt", 'r') as fp:
            for line in fp:
                #command, time, x, y
                command = line.split()
                for i in range(int(command[1])):
                    if len(command) == 2:
                        self.notes.append([command[0]])
                    else:
                        self.notes.append([command[0], command[2], command[3]])

    def onFrame(self, frame, direction):
        now = time.time()
        if (now - self.startTime) / self.secondsPerBeat > self.beatsDone + 1:
            #Onto a new beat.
            self.beatsDone += 1
            print("Beat: " + str(self.beatsDone))

        currentlyPlaying, currentlyPlayingX, currentlyPlayingY = self.getCurrentNote()

        font = cv2.FONT_HERSHEY_SIMPLEX
        if currentlyPlaying == direction:
            self.score += 1
        text = 'Score: ' + str(self.score)
        #img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]
        cv2.putText(frame, text, (10, 450), font, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        green = (0,255,0)
        yellow = (0,255,255)
        if (currentlyPlaying != 'wait'):
            vision.drawDirection(frame, currentlyPlayingX, currentlyPlayingY, currentlyPlaying, green)

        timeSinceLastBeat = (now - self.startTime) % self.secondsPerBeat
        #Next four beats, draw upcoming letters
        beatsInFuture = 0
        newNote = None
        while (newNote is None):
            beatsInFuture += 1
            currentNote = self.notes[self.beatsDone+beatsInFuture][0]
            if currentNote != 'wait' and currentNote != currentlyPlaying:
                newNote = currentNote

        x, y = int(self.notes[self.beatsDone + beatsInFuture][1]), int(self.notes[self.beatsDone + beatsInFuture][2])
        secondCircleRadius = 40  # The default
        secondCircleRadius *= beatsInFuture + ((self.secondsPerBeat - timeSinceLastBeat)/self.secondsPerBeat)
        # secondCircleRadius *= 4 - (beatsInFuture + 1 + (timeSinceLastBeat / self.secondsPerBeat))
        vision.drawDirection(frame, x, y, newNote, yellow, secondCircleRadius=int(secondCircleRadius))


    def getCurrentNote(self):
        currentlyPlaying = self.notes[self.beatsDone][0]
        currentlyPlayingX = None
        currentlyPlayingY = None
        if (currentlyPlaying != 'wait'):
            currentlyPlayingX = int(self.notes[self.beatsDone][1])
            currentlyPlayingY = int(self.notes[self.beatsDone][2])
        return currentlyPlaying, currentlyPlayingX, currentlyPlayingY


