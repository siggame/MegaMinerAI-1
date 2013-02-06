///////////////////////////////////////////////////////////////////////////////
/// @file   exampleAI.h
///
/// @author Ben
///
/// @brief  Example AI header
///////////////////////////////////////////////////////////////////////////////

#ifndef _EXAMPLEAI_H_
#define _EXAMPLEAI_H_

#include <string>
#include <vector>
#include "../baseAI.h"
#include "../client-structures.h"

///////////////////////////////////////////////////////////////////////////////
/// @class  myAI
///
/// @brief  Example AI for competitors to look at
///////////////////////////////////////////////////////////////////////////////
class myAI : public baseAI
{
   public:
   
      myAI();
      ~myAI();

      void Play();
      string PlayerName();
   
      //From baseAI
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
      
      
      //void BuyUnit(unitInfo* typeToBuy);
      //void Move(const unit& toMove, const coordinate& moveTo);
      //void Attack(const unit& attackWith, const coordinate& attackCoord);
      //void Gather(const unit& toGather);
   
};





#endif
