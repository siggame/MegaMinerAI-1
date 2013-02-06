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
    minCost = unitTypes[0].getCost();
    for(int i=0; i < unitTypes.size(); i++)
    {
        if(unitTypes[i].getCost() < minCost)
            minCost = unitTypes[i].getCost();
    }
    nextPurchase = 0;
    
    center = coordinate(12,13);

}

//Cleanup
myAI::~myAI()
{

}

      //vector<unit> myUnits;          //Vector of AI's units on the map
      //vector<unit> enemyUnits;       //Vector of enemy units on the map
      //vector<base> bases;            //Vector of bases on the map
      //vector<resource> resourceNodes;//Vector of resource nodes on the map
      //vector<unitInfo> unitTypes;    //Vector of unit types
      //long myScore;      //Score of the AI
      //long enemyScore;   //Score of the enemy
      //int turnNumber;    //Current turn number
      //int maxTurns;      //The turn number that ends the game
      
      
      //void BuyUnit(unitInfo* typeToBuy);
      //void Move(const unit& toMove, const coordinate& moveTo);
      //void Attack(const unit& attackWith, const coordinate& attackCoord);
      //void Gather(const unit& toGather, const coordinate& attackCoord);


//Play function, called at the start of every turn
void myAI::Play()
{
    long credits = myScore;

    if(unitTypes[nextPurchase].getCost() <= credits)
    {
    
        credits -= unitTypes[nextPurchase].getCost();
        
        BuyUnit(&unitTypes[nextPurchase]);
        
        nextPurchase++;
        if(nextPurchase >= unitTypes.size()) 
        {
            nextPurchase = 0;
        }
    }
     
    for(int j=0; j < 3; j++)
    {   
        for(int i=0; i < myUnits.size(); i++)
        {
            if(myUnits[i].getMoves() > 0)
            {
                unitAction(&myUnits[i]);    
            }
        
        }
    }

   return;
}

void myAI::unitAction(unit* fighter)
{
    int distance;
    bool tookAction = false;

    if(fighter->distanceTo(center) > 3)
    {
        moveToward(fighter, center);
        tookAction = true;
    }
    
    if(!tookAction)
    {
        coordinate enemyLoc = nearestEnemy(fighter);
        distance = fighter->distanceTo(enemyLoc);
        
        if(distance <= fighter->constants->getAttackRange())
        {
            Attack(*fighter, enemyLoc);
            tookAction = true;
        }
    }
    
    if(!tookAction)
    {
        coordinate resourceLoc = nearestResource(fighter);
        distance = fighter->distanceTo(resourceLoc);
        
        if(distance <= 1)
        {
            Gather(*fighter,resourceLoc);
            tookAction = true;
        }
        else
        {
            moveToward(fighter, resourceLoc);
        }
    }

}

void myAI::moveToward(unit* toMove, const coordinate& moveTo)
{
    coordinate curLoc = toMove->getLocation();
    coordinate desired = curLoc - moveTo;
    
    if(desired.x > 0)
        desired.x = min(desired.x, 1);
    else
        desired.x = -min(-desired.x,1);

    if(desired.y > 0)
        desired.y = min(desired.y, 1);
    else
        desired.y = -min(-desired.y,1);
    
    curLoc = curLoc - desired;
    
    Move(*toMove, curLoc);
}


coordinate myAI::nearestEnemy(unit* toFind)
{
    coordinate unitLoc = toFind->getLocation();
    
    coordinate nearest;
    
    int minDist = 100;
    int tempDist = 0;
    
    for(int i=0; i < enemyUnits.size(); i++)
    {
        tempDist = enemyUnits[i].distanceTo(unitLoc);
        if(tempDist <= minDist)
        {
            minDist = tempDist;
            nearest = enemyUnits[i].getLocation();
        }
    }
    return nearest;
}


coordinate myAI::nearestResource(unit* toFind)
{
    coordinate unitLoc = toFind->getLocation();
    
    coordinate nearest;
    
    int minDist = 100;
    int tempDist = 0;
    
    for(int i=0; i < resourceNodes.size(); i++)
    {
        tempDist = toFind->distanceTo(resourceNodes[i].getLocation());
        if(tempDist <= minDist)
        {
            minDist = tempDist;
            nearest = resourceNodes[i].getLocation();
        }
    }
    return nearest;
}

//Return your name
string myAI::PlayerName()
{
   return string("Ben Test AI");
}




















