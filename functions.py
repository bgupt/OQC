import numpy as np


def gates_and_angles(in_string):
    '''
    input:
    
        in_string (string) : input gate string with angle parameter
        
    output:
        gates: list of gate string
        angles: list of corresponding angles
    '''
    
    ops = [item.strip() for item in in_string.split(',')]

    angles_in = [int(item[2:-1]) for item in ops]
    gates_in = [item[0] for item in ops]

    tmp1 = gates_in[0]
    split = []
    tmp = []
    for i, item in enumerate(gates_in):
        tmp2 = item

        if tmp2 == tmp1:
            tmp.append((tmp2, angles_in[i]))
        else:
            split.append(tmp)
            tmp = [(item, angles_in[i])]
            tmp1 = item
        if i == len(gates_in)-1:
            split.append(tmp)

    tmp = ""

    angles = []
    gates = []
    for i, item in enumerate(split):
        angles.append(np.fmod(np.sum([j for i, j in item]), 360))
        gates.append(item[0][0])
    
    return gates, angles


def part_1(in_string):
    '''
    Optimizes single qubit X, Y and Z gates by combining them in fewer gates.
    
    input:
    
        in_string (string) : input gate string with angle parameter
        
    output:
        string: optimized gate string
    '''

    
    gates, angles = gates_and_angles(in_string)
    
    delete_idx = np.zeros(len(gates)).astype(int)
    
    for i in range(1,len(gates)):
        if angles[i] == 180 and angles[i-1] == angles[i+1]:
            delete_idx[i] = 1

    final_config = []

    for i in range(len(gates)):

        if delete_idx[i] == 1:
            gates[i-1] = 0
            angles[i-1] = 0
            gates[i+1] = 0
            angles[i+1] = 0

            if i+2 < len(gates):
                print("Here!")
                gates[i+2] = 0
                anlges[i] = angles[i] + angles[i+2]

            i += 2

    final_config = [item+"({})".format(angles[i]) for i, item in enumerate(gates) if item!=0]
    
    string = ""# flattened_gates[0]+"({})".format(flattened_angles[0])
    
    for i in range(len(gates)):
         if gates[i] != 0:
            if i == len(gates)-1:
                string += str(gates[i])+'({})'.format(angles[i])
            else:
                string += str(gates[i])+'({}), '.format(angles[i])
    
    
    if string[-2] == ",":
        string = string[:-2]

    
    return string


def part_2(in_string):
    '''
    Similar to function part_1(). Optimizes single qubit X, Y and Z gates. Replaces Y gate with Z.X.Z format and then optimizes.
    
    input:
    
        in_string (string) : input gate string with angle parameter
        
    output:
        string: optimized gate string
    '''


    gates, angles = gates_and_angles(in_string)
    
    new_gates = gates
    new_angles = np.array(angles)
    new_angle_tmp = list(new_angles)

    for i, item in enumerate(gates):
        if item=='Y':
            new_gates[i] = ['Z', 'X', 'Z']
            new_angle_tmp[i] = [90, angles[i], -90]

    flattened_gates = [item for sublist in new_gates for item in sublist]

    flattened_angles = []

    for item in new_angle_tmp:
        if isinstance(item, list):
            for term in item:
                flattened_angles.append(term)
        else:
            flattened_angles.append(item)

    string = ""# flattened_gates[0]+"({})".format(flattened_angles[0])
    
    for i in range(len(flattened_gates)):
        if i == len(flattened_gates)-1:
            string += flattened_gates[i]+'({})'.format(flattened_angles[i])
        else:
            string += flattened_gates[i]+'({}), '.format(flattened_angles[i])
    
    string = part_1(string)
   

    return part_1(string)


def part_3(in_string, LengthZ, LengthX):
    '''
    OPtimization of gates done in part_2(). This function computes the total gate time of optimized circuit. 
    
    input:
    
        in_string (string) : input gate string with angle parameter
        LengthZ (int): Z Gate time length
        LengthX (int): X Gate time length
        
    output:
        string: optimized gate string
        gate_time: final optimized gate time.
    '''

    g, a = gates_and_angles(part_2(in_string))
    
    gate_time = 0
    
    for item in g:
        
        is_X = int(item == 'X')
        is_Z = int(item == 'Z')
        
        gate_time += is_X * LengthX + is_Z * LengthZ
    
    
    return part_2(in_string), gate_time
    
    
def gates_qubits_and_angles(in_string):
    '''
    input:
    
        in_string (string) : input gate string with angle and qubit parameter
        
    output:
        gates: list of gate string
        qubits: list of qubits acted upon
        angles: list of corresponding angles
    '''

    
    ops_in = [item.strip() for item in in_string.split('),')]

    gates_in = [item.split("(")[0].split(")")[0] for item in ops_in]
    angles_in = [int(item.split("(")[1].split(")")[0][3:]) for item in ops_in]
    qubits_in = [int(item.split("(")[1].split(")")[0][0]) for item in ops_in]

    for i in range(len(gates_in)-1):
        if gates_in[i] == 'CX' and gates_in[i+1] == 'X':
            if i > 0 and gates_in[i-1] != 'CX':
                gates_in[i], gates_in[i+1] = gates_in[i+1], gates_in[i]
                angles_in[i], angles_in[i+1] = angles_in[i+1], angles_in[i]
                qubits_in[i], qubits_in[i+1] = qubits_in[i+1], qubits_in[i]
            if i == 0:
                gates_in[i], gates_in[i+1] = gates_in[i+1], gates_in[i]
                angles_in[i], angles_in[i+1] = angles_in[i+1], angles_in[i]
                qubits_in[i], qubits_in[i+1] = qubits_in[i+1], qubits_in[i]

                
    tmp1 = gates_in[0]
    tmp1_qubit = qubits_in[0]
    split = []
    tmp = [(gates_in[0], qubits_in[0], angles_in[0])]
    
    for i in range(1,len(gates_in)):
        tmp2 = gates_in[i]
        tmp2_qubit = qubits_in[i]
        tmp1_qubit = qubits_in[i-1]


        if tmp2 == tmp1 and qubits_in[i-1] == qubits_in[i] and tmp2 != 'CX':
            tmp.append((tmp2, qubits_in[i], angles_in[i]))
        elif qubits_in[i] == qubits_in[i-1] and angles_in[i] == angles_in[i-1] and tmp2 == 'CX':
            tmp = [("I", 0, 1)]
        else:
            split.append(tmp)
            tmp = [(gates_in[i], qubits_in[i], angles_in[i])]
            tmp1 = gates_in[i]
            
        if i == len(gates_in)-1:
            split.append(tmp)


    tmp = ""
    is_CX = [item == [("I", 0, 1)] for item in split]
    if any(np.array(is_CX)) == True:
        del split[split.index([("I", 0, 1)])]

    angles = []
    gates = []
    qubits = []
    for i, item in enumerate(split):
        angles.append(np.fmod(np.sum([k for ii, j, k in item]), 360))
        gates.append(item[0][0])
        qubits.append(item[0][1])
    
    
    return gates, qubits, angles


def part_4(in_string, length1Q, length2Q):
    '''
    Optimizes two qubit circuit with X, Z and CX gates by combining them. Then marks time stamp in the optimized circuit. 
    
    input:
    
        in_string (string) : input gate string with angle parameter.
        length1Q: Single qubit gate time of X and Z gates.
        length2Q: Single qubit gate time of CX gate.
        
    output:
        string: optimized gate string with qubit, angle and operation time marking. 
    '''


    
    gates, qubits, angles = gates_qubits_and_angles(in_string)
    
    delete_idx = np.zeros(len(gates)).astype(int)
    
    
    for i in range(len(gates)-1):
        if gates[i] == 'CX' and gates[i+1] == 'X':
            gates[i], gates[i+1] = gates[i+1], gates[i]
            angles[i], angles[i+1] = angles[i+1], angles[i]
            qubits[i], qubits[i+1] = qubits[i+1], qubits[i]
            

    for i in range(1,len(gates)):
        if angles[i] == 180 and qubits[i-1] == qubits[i+1] and gates[i-1] == gates[i+1]:
            if gates[i-1] != 'CX':
                delete_idx[i] = 1

    final_config = []

    for i in range(len(gates)):

        if delete_idx[i] == 1:
            gates[i-1] = 0
            angles[i-1] = 0
            gates[i+1] = 0
            angles[i+1] = 0

            if i+2 < len(gates):
                if gates[i+2] == gates[i]:
                    print("Here!")
                    gates[i+2] = 0
                    angles[i] = angles[i] + angles[i+2]

            i += 2
            
    
    final_config = []
    
    new_gates= []
    new_qubits= []
    new_angles= []
    
    for i, item in enumerate(gates):
        if item != 0:
            new_gates.append(gates[i])
            new_qubits.append(qubits[i])
            new_angles.append(angles[i])
        
    gate_time = 0
    
    for i, item in enumerate(new_gates):
        is_CX = int(item == 'CX') 
        final_config.append(item+"({}, {}, {})".format(new_qubits[i], new_angles[i], gate_time))
        gate_time +=  (1 - is_CX) * length1Q + is_CX * length2Q
    
    string = ""
    
    for item in final_config:
        string += item+", "
    
    string = string[:-2]
        
    return string
