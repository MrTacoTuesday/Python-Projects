from encryption import v2, test

#key = v2.new(shifts=4,shiftdeg=18,muldeg=4)
#key = v2(224208, 144646, 195640, 28749, mul = 14)
key = v2()
message = "Secret messages are cool."
test(key, message)


