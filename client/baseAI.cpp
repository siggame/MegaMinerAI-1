///////////////////////////////////////////////////////////////////////////////
/// @file   baseAI.cpp
///
/// @author Ben
///
/// @brief  base AI class implementation
///////////////////////////////////////////////////////////////////////////////

#include "baseAI.h"
#include <sstream>

///////////////////////////////////////////////////////////////////////////////
/// @brief  Default Constructor
///////////////////////////////////////////////////////////////////////////////     
baseAI::baseAI()
{
   myUnits.clear();
   enemyUnits.clear();
   resourceNodes.clear();
   unitTypes.clear();
   
   myScore = 0;
   enemyScore = 0;
   
   turnNumber = 0;
   maxTurns = 0;
}


///////////////////////////////////////////////////////////////////////////////
/// @brief Queues an order to buy a unit. Reduces your (local) score by the cost
///
/// @param typeToBuy A pointer to the unitInfo of the unit you want to purchase
///////////////////////////////////////////////////////////////////////////////  
void baseAI::BuyUnit(unitInfo* typeToBuy)
{
   sout.str("");
   
   //Convert to s-expression
   sout << "(game-build " << typeToBuy->getUnitType() << ")";
   myOrder.s_expression = sout.str();
   
   orders.push(myOrder);
   
   myScore -= typeToBuy->getCost();
   
   return;
}


///////////////////////////////////////////////////////////////////////////////
/// @brief Queues an order to move a unit. Reduces the unit's move count by one
///        and moves the (local unit) to moveTo. (Unit position updated by server each turn)
///
/// @param toMove The unit to move
/// @param moveTo The coordinate to move to. Non-adjacent coordinates to the 
///               unit's current location will cause the order to be rejected
///               by the server
/////////////////////////////////////////////////////////////////////////////// 
void baseAI::Move(unit& toMove, const coordinate& moveTo)
{
   sout.str("");
   
   //Convert to s-expression
   sout << "(game-move " << toMove.getID() << " " << moveTo.x << " " << moveTo.y << ")";
   myOrder.s_expression = sout.str();
   
   orders.push(myOrder);
   
   toMove.setMoves(toMove.getMoves()-1);
   toMove.setLocation(moveTo);
   
   return;
}


///////////////////////////////////////////////////////////////////////////////
/// @brief Queues an attack order for a unit. Reduces the unit's move count by 1
///
/// @param attackWith The unit that will attack
/// @param attackCoord The location to attack
/////////////////////////////////////////////////////////////////////////////// 
void baseAI::Attack(unit& attackWith, const coordinate& attackCoord)
{
   sout.str("");
   
   //Convert to s-expression
   sout << "(game-attack " << attackWith.getID() << " " << attackCoord.x << " " << attackCoord.y << ")";
   myOrder.s_expression = sout.str();
   
   orders.push(myOrder);
   
   attackWith.setMoves(attackWith.getMoves()-1);
   
   for(int i=0; i < enemyUnits.size(); i++)
   {
      if(enemyUnits[i].getLocation() == attackCoord)
      {
         enemyUnits[i].setHealth(enemyUnits[i].getHealth()-attackWith.constants->getAttackPower());
         myScore += (int)resourceNodes[i].getMultiplier();
      }
   }
   
   return;
}


///////////////////////////////////////////////////////////////////////////////
/// @brief Queues an order for a unit to gather resources. Reduces the unit's move count by one
///
/// @param toGather The unit that will gather
/// @param gatherCoord The coordinate to gather from
/////////////////////////////////////////////////////////////////////////////// 
void baseAI::Gather(unit& toGather, const coordinate& gatherCoord)
{
   sout.str("");
   
   //Convert to s-expression
    sout << "(game-gather " << toGather.getID() << " " << gatherCoord.x << " " << gatherCoord.y << ")";
   myOrder.s_expression = sout.str();
   
   orders.push(myOrder);
   
   toGather.setMoves(toGather.getMoves()-1);
   
   for(int i=0; i < resourceNodes.size(); i++)
   {
      if(resourceNodes[i].getLocation() == gatherCoord)
      {
         resourceNodes[i].setRemaining(resourceNodes[i].getRemaining()-1);
         myScore += (int)resourceNodes[i].getMultiplier();
      }
   }
   
   return;
}


///////////////////////////////////////////////////////////////////////////////
/// @brief Release acquired resources
///////////////////////////////////////////////////////////////////////////////
baseAI::~baseAI()
{
   return;
}
