///////////////////////////////////////////////////////////////////////////////
/// @file   shellAI.cpp
///
/// @author Ben
///
/// @brief  Shell API implementation file for competitors to fill out
///////////////////////////////////////////////////////////////////////////////

#include "shellAI.h"
#include <iostream>
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
   for(int i = 0; i < 50; i++)
   {
   	BuyUnit(&unitTypes[0]);
   }

	for(int i=0; i < myUnits.size(); i++)
	{
	    myUnits[i].setLocation(myUnits[i].getLocation() + coordinate(rand()%2,rand()%2));
		Move(myUnits[i], myUnits[i].getLocation());
		Move(myUnits[i], (myUnits[i].getLocation() + coordinate(rand()%2,rand()%2)));
	}
	
	/*
	queue<order> tosend = orders;
	while( tosend.size() != 0)
	{
			
				string myOrder = tosend.front().s_expression;
				tosend.pop();
				cout << myOrder << endl;
	}
	*/
	
   return;
}

//Return your name
string myAI::PlayerName()
{
   return string("Example AI");
}
