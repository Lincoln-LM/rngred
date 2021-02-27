def multby5(a):         # Replicate MultBy5 function in rngred
    b = a               # ld b,a
    b = b<<2            # SLA b; SLA b
    b += a              # ADD a
    return b & 0xFF     # convert to byte

def next(seed):         # Replicate RNG function in rngred
    a = seed            # ld a,seed
    a = multby5(a)      # call multby5
    a += 13             # add 13
    return a & 0xFF     # convert to byte

def next_quick(seed):
    return (seed*5+13) & 0xFF


substates = []
subseed = 1
addstates = []
addseed = 0
for _ in range(255):
    substate = hex(subseed)[2:].zfill(2)
    substates.append(substate)
    subseed = next(subseed)
for _ in range(256):
    addstate = hex(addseed)[2:].zfill(2)
    addstates.append(addstate)
    addseed = next(addseed)

def quick_state_to_frame(state): # quick way to get frame from state
    subindex = substates.index(state[:2])
    addindex = addstates.index(state[2:])
    subperiod = (subindex-addindex) & 0xFF
    if addindex >= 256-subperiod:
        add = -(256-addindex)
    else:
        add = addindex
    frame = subperiod*256+add
    return frame

def quick_frame_to_state(frame): # quick way to get state from frame
    seed = 0
    seed1 = 1
    addindex = frame%256
    for _ in range(addindex):
        seed = next_quick(seed)
    
    subindex = frame%255
    for _ in range(addindex+(subindex-addindex)):
        seed1 = next_quick(seed1)

    return(hex(seed1 << 8 | seed)[2:].zfill(4))

def state_to_seeds(state):
    return int(state[:2],16), int(state[2:],16)

def reverse_state_to_dvs(state):
    return int(state[0],16), int(state[1],16), int(state[2],16), int(state[3],16)

def tid_to_state(tid):
    return hex(tid)[2:].zfill(4)

def dvs_to_state(dvs):
    return hex(dvs[0]<<4 | dvs[1] | dvs[2]<<12 | dvs[3]<<8)[2:].zfill(4)

if __name__ == "__main__":
    while True:
        print("Frame View:0, State to Frame:1, TID to Frame:2, DVs to Frame:3, Calculate Visual Frame:4, Exit:5")
        choice = int(input(":"))
        if choice == 0:
            starting_frame = int(input("Starting Frame:"))
            total_frames = int(input("Total Frames:"))

            sub_seed, add_seed = state_to_seeds(quick_frame_to_state(starting_frame))

            print("Frame, State, DVs, TID")
            for frame in range(total_frames):
                if next(sub_seed) == 1:
                    sub_seed = next(sub_seed)
                state = hex(sub_seed << 8 | add_seed)[2:].zfill(4)
                reverse_state = hex(add_seed << 8 | sub_seed)[2:].zfill(4)
                print(frame+starting_frame, state, reverse_state_to_dvs(reverse_state), int(state,16))
                add_seed = next(add_seed)
                sub_seed = next(sub_seed)
        elif choice == 1:
            state = input("State:").lower()
            print("Frame:", quick_state_to_frame(state))
        elif choice == 2:
            tid = int(input("TID:"))
            state = tid_to_state(tid)
            print("Frame:", quick_state_to_frame(state))
        elif choice == 3:
            dvstring = input("DVs (ATK.DEF.SPE.SPC):")
            dvs = []
            for dv in dvstring.split("."):
                dvs.append(int(dv))
            state = dvs_to_state(dvs)
            print("Frame:", quick_state_to_frame(state))
        elif choice == 4:
            visual_frame = int(input("Visual Frame:"))
            target_frame = int(input("Target Frame:"))
            current_state = input("Current State:").lower()
            current_frame = quick_state_to_frame(current_state)
            delay = int(input("Delay:"))

            while target_frame < current_frame:
                target_frame += 0xFF00
            
            calibration = visual_frame-current_frame
            target_visual_frame = target_frame + calibration
            target_visual_frame -= delay
            print("Target Visual Frame",target_visual_frame)
        else:
            break
