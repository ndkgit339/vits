from pathlib import Path
from sklearn.model_selection import train_test_split
import argparse

if __name__ == "__main__":
    def get_parser():
        parser = argparse.ArgumentParser(
            description="Prepare filelist for jvs dataset.")
        parser.add_argument(
            "--jvs_path", type=str, default="",
            help="Path to jvs dataset.")
        return parser
    
    args = get_parser().parse_args()

    train, val, test = [], [], []
    for spk_path in Path(args.jvs_path).glob("jvs*"):
        spk = spk_path.name
        spk = int(spk.split("jvs")[1]) - 1
        data_spk = []
        for data_type in ["parallel100", "nonpara30"]:
            wav_dir = spk_path / data_type / "wav24kHz16bit"
            tr_path = spk_path / data_type / "transcripts_utf8.txt"
            with open(tr_path, "r") as f:
                for l in f:
                    basename, text = l.strip().split(":")
                    wav_path = wav_dir / f"{basename}.wav"
                    if wav_path.exists():
                        wav_path = str(wav_path)
                        data_spk.append(
                            f"{wav_path}|{spk}|{text}")
            
        train_spk, test_spk = train_test_split(data_spk, test_size=3, random_state=42)
        train_spk, val_spk = train_test_split(train_spk, test_size=3, random_state=42)
        
        train.extend(train_spk)
        val.extend(val_spk)
        test.extend(test_spk)

    with open("filelists/jvs_audio_sid_text_train_filelist.txt", "w") as f:
        f.write("\n".join(train))
    with open("filelists/jvs_audio_sid_text_val_filelist.txt", "w") as f:
        f.write("\n".join(val))
    with open("filelists/jvs_audio_sid_text_test_filelist.txt", "w") as f:
        f.write("\n".join(test))
        