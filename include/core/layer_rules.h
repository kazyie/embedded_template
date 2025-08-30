// include/core/layer_rules.h
#pragma once
#if defined(CURRENT_LAYER_APP)
  #define LAYER_APP 1
#elif defined(CURRENT_LAYER_MW)
  #define LAYER_MW 1
#elif defined(CURRENT_LAYER_DRV)
  #define LAYER_DRV 1
#else
  #define LAYER_APP 0
  #define LAYER_MW  0
  #define LAYER_DRV 0
#endif
