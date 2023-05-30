from crc import Calculator, Crc32

TERM_SEQ = '01111110'
FRAME_SIZE = 32

def addCRC(message):
    calculator = Calculator(Crc32.CRC32)
    checksum = calculator.checksum(bytes(message, 'utf-8'))
    calced_crc = ""
    calced_crc += str(format(checksum, 'b'))
    while len(calced_crc) < 32 :
        calced_crc = "0" + calced_crc
    return message + calced_crc

def encode():
    count = 0
    stream = ""
    output_string = ""
    with open("origin.txt",'r') as f:
        stream = f.readline()
        print(f"origin:  {stream}")
    with open("encoded.txt",'w') as f:
        while len(stream) != 0 :
            if len(stream) >= FRAME_SIZE:
                output_string = stream[:FRAME_SIZE]
                stream = stream[FRAME_SIZE:]
            else:
                output_string = stream
                stream = ""
            output_string = addCRC(output_string)
            output_string = output_string.replace("11111", "111110")
            output_string = TERM_SEQ + output_string + TERM_SEQ
            #print(f"output_string: {output_string}")
            f.write(output_string)
            count += 1
    print(f"frames sent = {count}")
        
def decode():
    calculator = Calculator(Crc32.CRC32)
    encoded = ""
    with open("encoded.txt",'r') as f:
        encoded = f.readline()
        print(f"encoded: {encoded}")
    frames = []
    frames = encoded.split(TERM_SEQ+TERM_SEQ)
    frames = [x.replace(TERM_SEQ, "") for x in frames]
    print(f"frames recived = {len(frames)}")
    with open("decoded.txt",'w') as f:
        for frame in frames:
            frame = frame.replace("111110", "11111")
            crcRec = frame[(len(frame) - 32):]
            frame = frame[:(len(frame) - 32)]
            if calculator.verify(bytes(frame, 'utf-8'), int(bytes(crcRec, 'utf-8'), 2)):
                f.write(frame)
    with open("decoded.txt",'r') as f:
        print(f"decoded: {f.read()}")
    with open("origin.txt",'r') as f:
        print(f"origin:  {f.read()}")

def main():
    encode()
    decode()

if __name__ == "__main__":
    main()