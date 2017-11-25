assignments = []
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    unitlistForNaked = row_units + column_units + square_units
    for unit in unitlistForNaked:
        tempDict = {}
        for key in unit:
            if values[key] in tempDict:
                tempDict[values[key]] += 1
            else:
                tempDict[values[key]] = 1
            for valueOccured, numberOfOcurance in tempDict.items():
                if numberOfOcurance >= 2 and len(valueOccured)==2:
                    for key in unit:
                        if values[key] !=valueOccured:
                            for digit in list(valueOccured):
                                assign_value(values, key, values[key].replace(digit, ""))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    result = []
    for a in A:
        for b in B:
            result.append(a+b)
    return result

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    dict = {};
    for i in range(0, len(grid)):
        if(grid[i] == '.'):
            dict[boxes[i]] = '123456789';
        else:
            dict[boxes[i]] = grid[i];
    return dict;

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for key, value in values.items():
        if(len(value)==1):
            rowNumber=rows.index(key[:1])
            coloumnNumber=cols.index(key[1:])
            squareNumber = (int(rowNumber/3))*3 + (int(coloumnNumber/3))
            keyRowUnit=row_units[rowNumber]
            keyColUnit=column_units[coloumnNumber]
            keySquareUnit=square_units[squareNumber]
            boxInDiagonal = False
            boxInTwoDiagonal = False
            if rowNumber == coloumnNumber  and (rowNumber + coloumnNumber) == 8:
                boxInDiagonal = True
                boxInTwoDiagonal = True
            elif rowNumber == coloumnNumber :
                keyDiagonalUnit = diagonal_units[0] ##first diagonal
                boxInDiagonal = True
            elif (rowNumber + coloumnNumber) == 8 :  
                keyDiagonalUnit = diagonal_units[1] ##second diagonal
                boxInDiagonal = True
            
            for i in range(0,9):
                if(len(values[keySquareUnit[i]]) !=1):
                    #values[keySquareUnit[i]]=values[keySquareUnit[i]].replace(value,"")
                    assign_value(values, keySquareUnit[i], values[keySquareUnit[i]].replace(value,""))
                if(len(values[keyRowUnit[i]]) !=1):
                    #values[keyRowUnit[i]]=values[keyRowUnit[i]].replace(value,"")
                    assign_value(values, keyRowUnit[i], values[keyRowUnit[i]].replace(value,""))
                if(len(values[keyColUnit[i]]) !=1):
                    #values[keyColUnit[i]]=values[keyColUnit[i]].replace(value,"")
                    assign_value(values, keyColUnit[i], values[keyColUnit[i]].replace(value,""))
                if boxInDiagonal:
                    if boxInTwoDiagonal:
                        for keyDiagonalUnit in diagonal_units:
                            if(len(values[keyDiagonalUnit[i]]) !=1):
                                #values[keyColUnit[i]]=values[keyColUnit[i]].replace(value,"")
                                assign_value(values, keyDiagonalUnit[i], values[keyDiagonalUnit[i]].replace(value,""))
                    else:
                        if(len(values[keyDiagonalUnit[i]]) !=1):
                            #values[keyColUnit[i]]=values[keyColUnit[i]].replace(value,"")
                            assign_value(values, keyDiagonalUnit[i], values[keyDiagonalUnit[i]].replace(value,""))
   
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            occurancce = []
            for box in unit:
                if digit in values[box]:
                    occurancce.append(box)
            if(len(occurancce) ==1):
                assign_value(values, occurancce[0], digit)
    return values

def reduce_puzzle(values):  
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        
        #Your code here: use Naked Twins
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    allValuesOne = True
    for key, value in values.items():
        if(len(value) != 1):
            allValuesOne = False
            break
    if allValuesOne ==True:
        return values
            
    # Choose one of the unfilled squares with the fewest possibilities
    lowestLen = 9
    lowestKey = None;
    for key, value in values.items():
        if(len(value) < lowestLen and len(value) != 1):
            lowestLen = len(value)
            lowestKey = key
  
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[lowestKey]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, lowestKey, value)
        ##search for new results
        returnedResults = search(new_sudoku)
        sameValueInDiagonal = False
        if returnedResults !=None and  returnedResults != False:
            #check for two equal values in same unit
            for unit in unitlist:
                tempDict = {}
                for key in unit:
                    if returnedResults[key] in tempDict:
                        #print(tempDict)
                        sameValueInDiagonal = True
                        break
                    else:
                        tempDict[returnedResults[key]] = 1
                if sameValueInDiagonal:
                    break
            if sameValueInDiagonal:
                continue
            else:
                return returnedResults
    return None

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
   
    values = grid_values(grid)
    values = search(values)
   
    return values

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = []
diagonal_units.append([r+c for r, c in zip(rows, cols)])
diagonal_units.append([r+c for r, c in zip(rows, reversed(cols))])
unitlist = diagonal_units + row_units + column_units + square_units  

if __name__ == '__main__':
    diag_sudoku_grid = '...7.9....85...31.2......7...........1..7.6......8...7.7.........3......85.......'
    returnedResults = solve(diag_sudoku_grid)
    display(returnedResults)
    
    """
    i=1;
    for unit in unitlist:
        tempDict = {}
        for key in unit:
            if returnedResults[key] in tempDict:
                print("error")
                tempDict[returnedResults[key]] += 1
            else:
                tempDict[returnedResults[key]] = 1
        print(str(i)+ " : "+str(tempDict))
        i=i+1
    
    """
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
            print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')