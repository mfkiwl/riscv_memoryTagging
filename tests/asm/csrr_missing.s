#include <defines.S>
#include <boot.S>


.text
main:
    csrr a0, pmpaddr15
    FAILED 1

ON_EXCEPTION:
    PASSED

