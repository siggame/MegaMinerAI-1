///////////////////////////////////////////////////////////////////////////////
/// @file   shellAI.cpp
///
/// @author Ben
///
/// @brief  Shell API implementation file for competitors to fill out
///////////////////////////////////////////////////////////////////////////////

#include "shellAI.h"
#include <iostream>
#include <cmath>
using namespace std;

//Initialization
myAI::myAI() : baseAI()
{

}

//Cleanup
myAI::~myAI()
{

}

      //void BuyUnit(unitInfo* typeToBuy);
      //void Move(const unit& toMove, const coordinate& moveTo);
      //void Attack(const unit& attackWith, const coordinate& attackCoord);
      //void Gather(const unit& toGather);

//Play function, called at the start of every turn
void myAI::Play()
{
    while(myScore > unitTypes[2].getCost())
    {
        BuyUnit(&unitTypes[2]);
    }

	for(int i=0; i < myUnits.size(); i++)
	{
        bool attacked = false;
      	for(int j=0; j < enemyUnits.size(); j++)
        {
            if(abs((int)enemyUnits[j].getLocation().x - (int)myUnits[i].getLocation().x) +
                abs((int)enemyUnits[j].getLocation().y - (int)myUnits[i].getLocation().y)
                < 5)
            {
                attacked = true;
                Attack(myUnits[i], enemyUnits[j].getLocation());
                Attack(myUnits[i], enemyUnits[j].getLocation());
                break;
            }
        }
        if(!attacked)
        {
            if(myUnits[i].getLocation().x < 25)
                Move(myUnits[i], myUnits[i].getLocation() + coordinate(1, 0));
            else
                Move(myUnits[i], myUnits[i].getLocation() + coordinate(0, 1));
        }
	}
	
   return;
}

//Return your name
string myAI::PlayerName()
{
   return string("Extreme AI");
}
