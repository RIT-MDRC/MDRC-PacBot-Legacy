#include <stdio.h>
#include <math.h>

double ForceA (double ForceX) {
    
    double ForceA = (2/3)*ForceX;
    
    return ForceA;
} 

double ForceB (double ForceX, double ForceY) {
    
    double ForceB = (-1/3)*ForceX - (1/sqrt(3))*ForceY;
    
    return ForceB;
} 

double ForceC (double ForceX, double ForceY) {
    
    double ForceC = (-1/3)*ForceX + (1/sqrt(3))*ForceY;
    
    return ForceC;
} 
int main()
{
    double ForceX;
    double ForceY;
    
    
    printf("Please input for Force X: ");
    scanf("%f", &ForceX);
    
    printf("Please input for Force Y: ");
    scanf("%f", &ForceY);
    
    ForceA(ForceX);
    ForceB(ForceX, ForceY);
    ForceC(ForceX, ForceY);
    
    return 0;
}

