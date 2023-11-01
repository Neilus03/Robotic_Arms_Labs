{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# We import the necessary libraries\n",
    "import sim           # library to connect with CoppeliaSim\n",
    "import sympy as sp   # library for symbolic calculation\n",
    "import numpy as np\n",
    "from sympy import *\n",
    "from sympy.physics.vector import init_vprinting\n",
    "from sympy.physics.mechanics import dynamicsymbols\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "init_vprinting(use_latex='mathjax', pretty_print=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "conectado a 19999\n",
      "24 22 17 19 21 0 0 0\n"
     ]
    }
   ],
   "source": [
    "\n",
    "\n",
    "\n",
    "# We define the symbolic variables\n",
    "theta1, theta2, d3, lc, la, lb, theta, alpha, a, d = dynamicsymbols('theta1 theta2 d3 lc la lb theta alpha a d')\n",
    "theta1, theta2, d3, lc, la, lb, theta, alpha, a, d \n",
    "\n",
    "def connect(port):\n",
    "# returns the client number or -1 if it cannot connect\n",
    "    sim.simxFinish(-1) # just in case, close all opened connections\n",
    "    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Connect\n",
    "    if clientID == 0: print(\"conectado a\", port)\n",
    "    else: print(\"no se pudo conectar\")\n",
    "    return clientID\n",
    "\n",
    "def setEffector(val):\n",
    "# function that triggers the end effector remotely\n",
    "# val is Int with value 0 or 1 to disable or activate the final actuator.\n",
    "    res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,\n",
    "        \"suctionPad\", sim.sim_scripttype_childscript,\"setEffector\",[val],[],[],\"\", sim.simx_opmode_blocking)\n",
    "    return res\n",
    "\n",
    "# We require the handlers for the joints, the suction cup and the suction sensor (Allows to know if the object is nearby)\n",
    "clientID = connect(19999)\n",
    "\n",
    "retCode,tip=sim.simxGetObjectHandle(clientID,'suctionPadSensor',sim.simx_opmode_blocking)\n",
    "retCode,suction=sim.simxGetObjectHandle(clientID,'suctionPad',sim.simx_opmode_blocking)\n",
    "retCode,joint1=sim.simxGetObjectHandle(clientID,'Joint1',sim.simx_opmode_blocking)\n",
    "retCode,joint2=sim.simxGetObjectHandle(clientID,'Joint2',sim.simx_opmode_blocking)\n",
    "retCode,joint3=sim.simxGetObjectHandle(clientID,'Joint3',sim.simx_opmode_blocking)\n",
    "retCode, blue = sim.simxGetObjectHandle(clientID,'blue',sim.simx_opmode_blocking)\n",
    "retCode, red = sim.simxGetObjectHandle(clientID,'red',sim.simx_opmode_blocking)\n",
    "retCode, green = sim.simxGetObjectHandle(clientID,'green',sim.simx_opmode_blocking)\n",
    "print(tip, suction, joint1, joint2, joint3, blue, red, green)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# We deactivate the final actuator (suction cup)\n",
    "setEffector(0)\n",
    "\n",
    "retCode,pos_red=sim.simxGetObjectPosition(clientID, red, -1, sim.simx_opmode_blocking)\n",
    "retCode,pos_green=sim.simxGetObjectPosition(clientID, green, -1, sim.simx_opmode_blocking)\n",
    "retCode,pos_blue=sim.simxGetObjectPosition(clientID, blue, -1, sim.simx_opmode_blocking)\n",
    "\n",
    "q = pos_green #posición Home and Collected Prism (Suction Cup Up)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/latex": [
       "$\\displaystyle \\left( 0.2 \\cos{\\left(\\theta_{1} + \\theta_{2} \\right)} + 0.2 \\cos{\\left(\\theta_{1} \\right)} - 1.19172072410583, \\  0.2 \\sin{\\left(\\theta_{1} + \\theta_{2} \\right)} + 0.2 \\sin{\\left(\\theta_{1} \\right)} - 0.444328516721725, \\  - d_{3} - 0.548503319740295\\right)$"
      ],
      "text/plain": [
       "(0.2*cos(theta1 + theta2) + 0.2*cos(theta1) - 1.19172072410583, 0.2*sin(theta1 + theta2) + 0.2*sin(theta1) - 0.444328516721725, -d3 - 0.548503319740295)"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dest_suction_cup = pos_green\n",
    "x, y, z = dest_suction_cup\n",
    "\n",
    "# eq1 is the one that gives us the value of the position X (eq=f(x)-x=0)\n",
    "eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x\n",
    "\n",
    "\n",
    "# eq2 is the one that gives us the value of the position Y (eq=f(y)-y=0)\n",
    "eq2 = (0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2)) - y\n",
    "\n",
    "\n",
    "# eq3 is the one that gives us the value of the position Z (eq=f(z)-z=0)   0.108 is the real height of manipulator\n",
    "eq3 = 0.108 - d3 - z\n",
    "\n",
    "\n",
    "\n",
    "eq1, eq2, eq3\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "q=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1))\n",
    "print(q)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "pytorch-env",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.18"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
