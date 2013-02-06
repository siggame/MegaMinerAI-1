///////////////////////////////////////////////////////////////////////////////
/// @file   shellAI.cpp
///
/// @author Ben
///
/// @brief  Example AI implementation
///////////////////////////////////////////////////////////////////////////////

#include "exampleAI.h"
///////////////////////////////////////////////////////////////////////////////
//vector<unit> myUnits;          //Vector of AI's units on the map
//vector<unit> enemyUnits;       //Vector of enemy units on the map
//vector<base> bases;            //Vector of bases on the map
//vector<resource> resourceNodes;//Vector of resource nodes on the map
//vector<unitInfo> unitTypes;    //Vector of unit types
//vector< vector<MAPNODE> > map; //Representation of map - 0 == empty, 1 == wall
//long myScore;      //Score of the AI
//long enemyScore;   //Score of the enemy
//int turnNumber;    //Current turn number
//int maxTurns;      //The turn number that ends the game
////////////////////////////////////////////////////////////////////////////////            
//void BuyUnit(unitInfo* typeToBuy);
//void Move(const unit& toMove, const coordinate& moveTo);
//void Attack(const unit& attackWith, const coordinate& attackCoord);
//void Gather(const unit& toGather);
////////////////////////////////////////////////////////////////////////////////

//Perform initialization in here
myAI::myAI() : baseAI()
{


}


//Perform cleanup here
myAI::~myAI()
{

}


void myAI::Play()
{
   //Buy whatever unitType 0 is - we need to tell them what each unit will be 
   //somehow
   BuyUnit(&unitTypes[0]);
   BuyUnit(&unitTypes[0]);
   BuyUnit(&unitTypes[0]);
   
   for(int i=0; i < myUnits.size(); i++)
   {
      if(i%4 == 0)
      {
         Move(myUnits[i], myUnits[i].getLocation()+coordinate(1,1));
      }
      
      if(i%4 == 1)
      {
         Attack(myUnits[i], myUnits[i].getLocation()+coordinate(myUnits[i].constants->getAttackRange(),0));
      }
      
      if(i%4 == 2)
      {
         Gather(myUnits[i]);
      }
      
      
   }
   return;
}

string myAI::PlayerName()
{
   return string("Ben's Example AI");
}
