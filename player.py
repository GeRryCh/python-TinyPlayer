import simpleaudio as sa
import wave
import os
import time

class Player:
    def __init__(self):
        #120 BPM; 1/8 note
        self.__note_length = 62.5

    def ___play_note(self, name):
        file_path = 'notes/' + name + '.wav'
        # return after note length if note not exists
        if not os.path.exists(file_path):
            # sleep receives seconds
            time.sleep(self.__note_length / 1000)
            return

        wave_read = wave.open(file_path, 'rb')
        audio_data = wave_read.readframes(wave_read.getnframes())
        num_channels = wave_read.getnchannels()
        bytes_per_sample = wave_read.getsampwidth()
        sample_rate = wave_read.getframerate()
        play_obj = sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
        play_obj.wait_done()


    def __parse_notes_file_into_array(self, file_path):
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

    def play_song(self, file_path):
        notes = self.__parse_notes_file_into_array(file_path)

        for note in notes:
            self.___play_note(note)
        print(notes)

def main():
    player = Player()
    player.play_song('songs/happy_birthday.txt')

if __name__ == '__main__':
    main()
