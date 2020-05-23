import simpleaudio as sa
import wave
import os
import time

note_length = 62.5


def play_note(name):
    file_path = 'notes/' + name + '.wav'
    # return after note length if note not exists
    if not os.path.exists(file_path):
        # sleep receives seconds
        time.sleep(note_length / 1000)
        return

    wave_read = wave.open(file_path, 'rb')
    audio_data = wave_read.readframes(wave_read.getnframes())
    num_channels = wave_read.getnchannels()
    bytes_per_sample = wave_read.getsampwidth()
    sample_rate = wave_read.getframerate()
    play_obj = sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    play_obj.wait_done()


def parse_notes_file_into_array(file_path):
    try:
        file = open(file_path, 'r')
        result = []
        for line in file:
            stripped_line = line.rstrip()
            result.extend(stripped_line.split(' '))
        file.close()
        return result
    except FileNotFoundError:
        print('Notes file: ' + file_path + " can't be found")
    except:
        print('Error in reading notes file: ' + file_path + "\nCheck if file format is correct")


def main():
    notes = parse_notes_file_into_array('songs/happy_birthday.txt')
    print(notes)


if __name__ == '__main__':
    main()
