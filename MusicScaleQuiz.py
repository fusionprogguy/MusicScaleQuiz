# Learn your major ('Major Scale') and minor scales ('Natural Minor Scale') in every key
# You can toggle showing the answer for testing the Music quiz with show_answer=True. Press F for False and T for True.
# You can swap between practicing the major scale or minor scale. Press MAJ and MIN for the Major and Natural Minor scale respectively.
# The loop goes indefinitely until you press spacebar as the answer. Press H to see a hint (number of sharps or flats)

import pandas
import random
from random import shuffle
import time

# Two Important variables for the Quiz
practice_scale = 'Natural Minor Scale'  # Name must match with data in scale_formula
show_answer = True  # Set to True for testing. Set to False to hide answers till you've made a guess.

# CODE BEGINS
print('Music Scale Quiz for the', practice_scale)
print('Press H for hint, and spacebar to quit')
print()

if show_answer:
    print('Showing chromatic scale, scale names, scale notes and answer for testing')
    print()

flat = ['♭', 'b']
sharp = ['♯', '#']

intervals = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7']
notes_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

scale_formula = {
    'Major Scale': '1 2 3 4 5 6 7',
    'Mixolydian': '1 2 3 4 5 6 b7',
    'Lydian': '1 2 3 b5 5 6 7',
    'Natural Minor Scale': '1 2 b3 4 5 b6 b7',
    'Aeolian b5': '1 2 b3 4 b5 b6 b7',
    'Mixolydian b6': '1 2 3 4 5 b6 b7',
    'Harmonic Minor': '1 2 b3 4 5 b6 7',
    'Melodic Minor': '1 2 b3 4 5 6 7',
    'Major Pentatonic': '1 2 3 5 6',
    'Minor Pentatonic': '1 b3 4 5 b7',
    'Blues Scale': '1 b3 4 b5 5 b7'
}

# Additional multiple choice scales to draw the possible answers from
other_major_scales = ['Mixolydian', 'Mixolydian b6', 'Lydian']           # Use these if 'Major Scale' is used,
other_minor_scales = ['Harmonic Minor', 'Melodic Minor', 'Aeolian b5']   # Use these if 'Natural Minor Scale' is used

chord_formula = {
    'Major triad': '1 3 5',
    'Minor triad': '1 b3 5',
}

def enharmonic(note):
    # Returns the opposite eg if given sharp note returns flat, if flat note is given returns sharp
    if note in notes_sharp:
        idx = notes_sharp.index(note)
        return notes_flat[idx]
    if note in notes_flat:
        idx = notes_flat.index(note)
        return notes_sharp[idx]

def randomise_scale(practice_scale, show_answer):
    # Select either the major scale or minor scale to practice in any key
    # You will get a multiple choice questions from similar scales
    global multiple_choice_scales
    global multiple_choice_notes
    global order

    # Use the other scales to get create the multiple choice questions
    other_scales = []
    if practice_scale == 'Major Scale':
        other_scales = other_major_scales[:]
    elif practice_scale == 'Natural Minor Scale':
        other_scales = other_minor_scales[:]

    # Filter only the scale you want to practice
    df_practice_scales = df[df['Scale'].str.contains(practice_scale)]   # '|'.join(endstrings)
    df_wrong_multiple_choice = df[df['Scale'].str.contains('|'.join(other_scales))]
    nscales = len(df_practice_scales)

    old_choices = []

    # Pick a random key + scale
    rand_choice = random.randint(0, nscales-1)
    # print(nscales, rand_choice)
    rand_scale_key = df_practice_scales.iloc[rand_choice]['Scale']
    rand_scale = ' '.join(rand_scale_key.split()[1:])
    rand_notes = df_practice_scales.iloc[rand_choice]['Notes']
    rand_key = rand_notes.split(' ')[0]

    if len(rand_key) == 1:
        key_scale = rand_key + ' ' + rand_scale
    else:
        key_scale = rand_key + '/' + enharmonic(rand_key) + ' ' + rand_scale

    print()
    print('Select your answer for the', key_scale, '(' + scale_formula[practice_scale] + ')')

    # Show the chromatic scale from the selected key eg D# would be: D# E F F# G G# A A# B C C# D
    start = 0
    end = 12
    found = 0
    collect_chromatic = []
    for idxr in range(0, 24):
        note = notes_sharp[idxr % 12]

        if found <= 2 and (note == rand_key or note == enharmonic(rand_key)):
            found += 1
            if found == 1:
                start = idxr
                end = start + 11

        if 1 <= found < 2 and note not in collect_chromatic:
            # print(note, intervals[(idxr - start) % 12])
            collect_chromatic.append(note)

        if idxr > end:
            break

    if show_answer:
        print(' '.join(intervals))
        print(' '.join(collect_chromatic))
        print()
        print('Multiple choice')

    filter_key = df_wrong_multiple_choice['Scale'].str.contains(rand_key+' ' + '|' + enharmonic(rand_key)+' ')   # Only look at the first 3 chars eg F##, Gb

    multiple_choice_scales = list(df_wrong_multiple_choice[filter_key]['Scale'])  # List of scales
    multiple_choice_notes = list(df_wrong_multiple_choice[filter_key]['Notes'])   # List of notes

    multiple_choice_scales.append(rand_scale_key)
    multiple_choice_notes.append(rand_notes)

    # Shuffle the order of multiple choice
    order = list(range(0, len(multiple_choice_scales)))
    shuffle(order)

    '''
    if show_answer:
        print(multiple_choice_scales)
        print(multiple_choice_notes)
        print()
        print('Rand order')
        print(order)
        print()
    '''

    # Find the right answer
    answer = '0'
    for idx, i in enumerate(order):
        if show_answer:
            scale_name = ' '.join(multiple_choice_scales[i].split()[1:])
            print(str(idx + 1) + ')', multiple_choice_scales[i] + ' (' + scale_formula[scale_name] + '): ' + multiple_choice_notes[i])
        else:
            print(str(idx + 1) + ')', multiple_choice_notes[i])

        if practice_scale in multiple_choice_scales[i]:
            answer = idx + 1
            hint = sum([1 if len(note)>1 else 0 for note in multiple_choice_notes[i].split()])
            # print(hint, multiple_choice_notes[i], len(multiple_choice_notes[i]))

    if show_answer:
        print('Answer:', answer)
    print()

    return answer, hint

score = 0
count = 0
hint = ''
guess = ''

df = pandas.read_csv('12-notes-scales.csv', header=0, names=['Scale', 'Notes'])
# print(df.to_string())

while True:
    count += 1
    if guess == 'H':
        print('Hint', hint, 'sharps/flats')
    elif guess == 'F':
        show_answer = False
        print('show_answer:', show_answer)
    elif guess == 'T':
        show_answer = True
        print('show_answer:', show_answer)
    else:
        if guess == 'MAJ':
            practice_scale = 'Major Scale'
        elif guess == 'MIN':
            practice_scale = 'Natural Minor Scale'

        answer, hint = randomise_scale(practice_scale, show_answer)  # Chooses a random key
    try:
        guess = input("Enter your guess: ").strip().upper()
        print()
        if len(guess) >= 1:
            if guess == 'H':
                continue
            elif guess == 'F':
                continue
            elif guess == 'T':
                continue
            elif guess == 'MAJ':
                continue
            elif guess == 'MIN':
                continue
            elif int(guess) == answer:
                print('Correct')
                score += 1
            else:
                print('Incorrect, the answer is ', answer)

            for idx, i in enumerate(order):
                print(str(idx + 1) + ')', multiple_choice_scales[i] + ': ' + multiple_choice_notes[i])

            print('Score:', str(score)+'/'+str(count))
            print('-----------')
            print()
            time.sleep(1.1)  # Wait a second before going to the next question
        else:  # Press spacebar to exit
            print('Score:', str(score) + '/' + str(count))
            print('Exiting Quiz')
            break

    except Exception as e:
        print(e)
        print()
