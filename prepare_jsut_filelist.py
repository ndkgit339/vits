import argparse
import pathlib 
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('jsut_path',type=str)
    args = parser.parse_args()
    output_lines = []
    transcript_files = pathlib.Path(args.jsut_path).glob("*/transcript_utf8.txt")
    for transcript_file in transcript_files:
        with open(transcript_file,mode='r') as f:
            lines = f.readlines()
        for line in lines:
            filename, text = line.split(':')
            output_lines.append('|'.join([
                str((transcript_file.parent/'wav'/filename).with_suffix('.wav')),
                text.strip('\n')
            ]))

    train_set, test_set = train_test_split(output_lines,train_size=0.9,random_state=42)
    train_set, val_set = train_test_split(output_lines,train_size=0.8,random_state=42)
    with open('filelists/jsut_audio_text_train_filelist.txt',mode='w') as f:
        f.write('\n'.join(train_set))
    with open('filelists/jsut_audio_text_val_filelist.txt',mode='w') as f:
        f.write('\n'.join(val_set))
    with open('filelists/jsut_audio_text_test_filelist.txt',mode='w') as f:
        f.write('\n'.join(test_set))

    

