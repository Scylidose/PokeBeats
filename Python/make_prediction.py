from music21 import converter, instrument, note, chord
import music21
from random import randint

import numpy as np

def generate_notes(model, net_inp, pitchnames, n_vocab, nb):
    start = np.random.randint(0, len(net_inp)-1)
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
    pattern = net_inp[start]
    prediction_output = []
  
    len_song = np.random.randint(300/nb, 600/nb)

    for note_index in range(len_song):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)
        prediction = model.predict(prediction_input, verbose=0)
        index = np.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)
        pattern = np.append(pattern, index)
        pattern = pattern[1:len(pattern)]

    return prediction_output

def transform_to_m21(prediction_output, type_song):
  offset = 0
  output_notes = []
  
  # create note and chord objects based on the values generated by the model
  for pattern in prediction_output:
      # pattern is a chord
      if ('.' in pattern) or pattern.isdigit():
          notes_in_chord = pattern.split('.')
          notes = []
          for current_note in notes_in_chord:
              new_note = note.Note(int(current_note))
              if  randint(0, 3, 1) == 0:
                new_note.storedInstrument = instrument.Trumpet()
              else:
                new_note.storedInstrument = instrument.Piano()
              notes.append(new_note)
          new_chord = chord.Chord(notes)
          new_chord.offset = offset
          output_notes.append(new_chord)
      # pattern is a note
      else:
          if randint(0, 10, 1) == 0:
            new_note = note.Rest()
            new_note.duration.quarterLength = 2
          else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            if  randint(0, 3, 1) == 0:
              new_note.storedInstrument = instrument.Trumpet()
            else:
              new_note.storedInstrument = instrument.Piano()
          output_notes.append(new_note)
      # increase offset each iteration so that notes do not stack
      if type_song == "Route" or type_song == "Buildings":
        offset += 0.5
      else:
        offset += 0.4
  print(len(output_notes))

  return output_notes