## Force-program
Here we use optimization to solve a toy physics problem. 
The solutions are my own but I stole the problem statement 
from Stephen Boyd's [textbook](http://vmls-book.stanford.edu/vmls.pdf).

With an $l_1$ penalty, the optimal force 
program is an impulse pair. Observe that 
forces applied early on give more 
"bang for buck" since the velocity 
is enjoyed for all future times.

A single thruster blast places
the mass in a ballistic phase, and
a retarding impulse brings the mass
to an instantaneous stop at the 
desired position.

![l_1](./images/l_1.png)

With an $l_2$ penalty, the optimal force 
program is a staircase.

![l_2](./images/l_2.png)

With an $l_{\infty}$ penalty, the optimal force 
program is constant on the two halves.

![l_inf](./images/l_inf.png)
