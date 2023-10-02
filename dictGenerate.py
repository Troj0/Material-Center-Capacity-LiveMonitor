buttonTexts = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L"]
buttonNumbers = ['01', '02', '03', '06', '07', '08']
buttonSuffix = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]

columns = range(2, 13)
rows = range(1, 24)

buttonPositions = {}

for col in columns:
    for row in rows:
        buttonIndex = (row - 1) % len(buttonTexts)
        buttonSuffixIndex = (col - 2) // 2
        buttonText = buttonTexts[buttonIndex]
        buttonNumber = buttonNumbers[buttonSuffixIndex]
        buttonSuffixIndex = buttonSuffixIndex * 2
        buttonSuffixValue = buttonSuffix[buttonSuffixIndex:buttonSuffixIndex + 2]
        buttonID = buttonNumber + buttonSuffixValue
        buttonPositions[buttonID] = (col, row)