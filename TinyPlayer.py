import simpleaudio as sa
import argparse as ap
import wave
import os
import time

class NotesFileParseException(Exception):
    """Raised when there's a problem parsing a note file"""
    pass

class Player:
    def __init__(self, bpm):
        self.__note_length = 60000/bpm/2
        # notes were recorded for 120BPM; 1/8 length = 60000/120/2
        self.__default_note_length = 250
        self.__rest_symbol = 'r'

    def __symbol_duration_ratio(self, symbol, symbol_length):
        if len(symbol) == symbol_length:
            return 1
        # take last
        duration_sign = symbol[-1]
        if duration_sign == '-':
            return self.__symbol_duration_ratio(symbol[:-1], symbol_length) / 2
        elif duration_sign == '+':
            return self.__symbol_duration_ratio(symbol[:-1], symbol_length) * 2
        elif duration_sign == '.':
            duration = self.__symbol_duration_ratio(symbol[:-1], symbol_length)
            duration += duration * 1/3
            return duration
        raise NotesFileParseException('Unrecognized length symbol: ' + duration_sign)

    def __play_note(self, note):
        def note_name(n):
            i = 0
            while i < len(n) and not n[i].isnumeric():
                i += 1

            return n[:i + 1]

        name = note_name(note)
        print("Playing: " + note)
        file_path = 'notes/' + name + '.wav'
        # return after note length if note not exists
        if not os.path.exists(file_path):
            raise NotesFileParseException("Sound file doesn't exist for symbol: " + note)

        wave_read = wave.open(file_path, 'rb')
        # note default length
        note_length_ratio = self.__symbol_duration_ratio(note, len(name))
        note_length = note_length_ratio * self.__note_length
        read_frames = wave_read.getnframes()
        if (note_length < self.__default_note_length):
            read_frames = int(read_frames * (note_length / self.__default_note_length))
        audio_data = wave_read.readframes(read_frames)
        num_channels = wave_read.getnchannels()
        bytes_per_sample = wave_read.getsampwidth()
        sample_rate = wave_read.getframerate()
        play_obj = sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
        play_obj.wait_done()
        if (note_length > self.__default_note_length):
            print("Rest: " + str(note_length - self.__default_note_length) + "ms")
            time.sleep((note_length - self.__default_note_length) / 1000)

    def __play_rest(self, rest):
        rest_time = self.__note_length * self.__symbol_duration_ratio(rest, 1)
        print("Rest: " + str(rest_time) + "ms")
        # sleep receives seconds
        time.sleep(rest_time / 1000)

    def __parse_notes_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                result = []
                for line in file:
                    stripped_line = line.rstrip()
                    result.extend(stripped_line.split(' '))
                return result
        except FileNotFoundError:
            print('Notes file: ' + file_path + " can't be found")
            exit()

    def __is_rest(self, symbol):
        return symbol.startswith('r')

    def play_song(self, file_path):
        symbols = self.__parse_notes_file(file_path)
        for s in symbols:
            try:
                if self.__is_rest(s):
                    self.__play_rest(s)
                else:
                    self.__play_note(s)
            except NotesFileParseException as e:
                print(e)
                break


def main():
    parser = ap.ArgumentParser(description='Tiny Player')
    parser.add_argument("--song", required=True, help='path to song text file')
    parser.add_argument("--bpm", required=False, default=120, help='A tempo of a song. Default 120bpm')
    args = vars(parser.parse_args())
    player = Player(args["bpm"])
    player.play_song(args["song"])


if __name__ == '__main__':
    main()
