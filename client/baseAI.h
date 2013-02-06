///////////////////////////////////////////////////////////////////////////////
/// @file   baseAI.h
///
/// @author Ben
///
/// @brief  base AI class definition
///////////////////////////////////////////////////////////////////////////////

#ifndef _BASEAI_H_
#define _BASEAI_H_

#include <deque>
#include <string>
#include <queue>
#include <string>
#include <sstream>
#include "client-structures.h"

using namespace std;

///////////////////////////////////////////////////////////////////////////////
/// @class  baseAI
///
/// @brief  Implements the baseAI class that the client uses to pass and take
///         variables. Includes pure virtual functions for the AI creators to
///         implement.
///////////////////////////////////////////////////////////////////////////////
class baseAI
{
   //variables
   public:
   
      //Inputs
      //Vectors for us to dump into
      deque<unit> myUnits;
      deque<unit> enemyUnits;
      deque<resource> resourceNodes;
      deque<unitInfo> unitTypes;
   
      long myScore;
      long enemyScore;
      
      coordinate myBase;
      coordinate enemyBase;

      int turnNumber; //Current turn number
      int maxTurns;   //The turn number that ends the game
	  
	  int playerNumber; // what player am I? 1? 2?

      //Outputs
      //Orders deque we will fill, then client will take from
      queue<order> orders;
     
   //Functions
   public:
      baseAI();
      ~baseAI();
   
      //Inputs
      virtual void Play() = 0;
      virtual string PlayerName() = 0;
      
      //Outputs
      void BuyUnit(unitInfo* typeToBuy);
      void Move(unit& toMove, const coordinate& moveTo);
      void Attack(unit& attackWith, const coordinate& attackCoord);
      void Gather(unit& toGather, const coordinate& gatherCoord);
      
   private:
      ostringstream sout;
      order myOrder;

};

#endif
