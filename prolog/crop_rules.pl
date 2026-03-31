/*
 * crop_rules.pl
 * -------------
 * Prolog Expert System for Crop Recommendation
 *
 * This knowledge base encodes agronomic rules about
 * soil nutrient levels and pH to reason about suitable crops.
 *
 * Usage (SWI-Prolog):
 *   swipl crop_rules.pl
 *   ?- recommend_crop(high, medium, high, neutral, Crop).
 *   ?- suitable_soil(rice, SoilType).
 *   ?- best_ph(coffee, Ph).
 *   ?- halt.
 */


/* =========================================================
   SECTION 1: Nutrient Level Classification
   =========================================================
   Nitrogen / Phosphorus / Potassium levels are:
     very_low | low | medium | high | very_high
   pH is:
     acidic | slightly_acidic | neutral | slightly_alkaline | alkaline
   ========================================================= */

% N levels (kg/ha approximate thresholds)
nitrogen_level(N, very_low)      :- N < 20.
nitrogen_level(N, low)           :- N >= 20,  N < 40.
nitrogen_level(N, medium)        :- N >= 40,  N < 80.
nitrogen_level(N, high)          :- N >= 80,  N < 120.
nitrogen_level(N, very_high)     :- N >= 120.

% P levels
phosphorus_level(P, very_low)    :- P < 10.
phosphorus_level(P, low)         :- P >= 10,  P < 25.
phosphorus_level(P, medium)      :- P >= 25,  P < 50.
phosphorus_level(P, high)        :- P >= 50,  P < 80.
phosphorus_level(P, very_high)   :- P >= 80.

% K levels
potassium_level(K, very_low)     :- K < 10.
potassium_level(K, low)          :- K >= 10,  K < 30.
potassium_level(K, medium)       :- K >= 30,  K < 60.
potassium_level(K, high)         :- K >= 60,  K < 100.
potassium_level(K, very_high)    :- K >= 100.

% pH categories
ph_level(Ph, acidic)             :- Ph < 5.5.
ph_level(Ph, slightly_acidic)    :- Ph >= 5.5, Ph < 6.5.
ph_level(Ph, neutral)            :- Ph >= 6.5, Ph < 7.5.
ph_level(Ph, slightly_alkaline)  :- Ph >= 7.5, Ph < 8.5.
ph_level(Ph, alkaline)           :- Ph >= 8.5.


/* =========================================================
   SECTION 2: Crop Soil Requirements (facts)
   Format:
     crop_needs(CropName, NitrogenLevel, PhosphorusLevel, PotassiumLevel, PhLevel)
   ========================================================= */

crop_needs(rice,         high,    medium,  medium,  slightly_acidic).
crop_needs(maize,        high,    high,    medium,  neutral).
crop_needs(chickpea,     low,     medium,  medium,  neutral).
crop_needs(kidneybeans,  medium,  medium,  medium,  neutral).
crop_needs(pigeonpeas,   medium,  low,     medium,  neutral).
crop_needs(mothbeans,    low,     low,     low,     slightly_alkaline).
crop_needs(mungbean,     medium,  medium,  medium,  slightly_acidic).
crop_needs(blackgram,    medium,  medium,  medium,  neutral).
crop_needs(lentil,       low,     medium,  medium,  neutral).
crop_needs(pomegranate,  medium,  medium,  medium,  neutral).
crop_needs(banana,       high,    high,    high,    slightly_acidic).
crop_needs(mango,        medium,  medium,  medium,  slightly_acidic).
crop_needs(grapes,       medium,  high,    high,    slightly_acidic).
crop_needs(watermelon,   high,    high,    high,    neutral).
crop_needs(muskmelon,    high,    high,    high,    neutral).
crop_needs(apple,        medium,  high,    high,    slightly_acidic).
crop_needs(orange,       high,    medium,  medium,  slightly_acidic).
crop_needs(papaya,       high,    medium,  medium,  slightly_acidic).
crop_needs(coconut,      medium,  medium,  high,    slightly_acidic).
crop_needs(cotton,       high,    medium,  medium,  neutral).
crop_needs(jute,         high,    medium,  medium,  neutral).
crop_needs(coffee,       high,    medium,  medium,  acidic).


/* =========================================================
   SECTION 3: Core Recommendation Rule
   =========================================================
   recommend_crop(+NLevel, +PLevel, +KLevel, +PhLevel, -Crop)
   Succeeds for every crop whose requirements match the inputs.
   ========================================================= */

recommend_crop(NLevel, PLevel, KLevel, PhLevel, Crop) :-
    crop_needs(Crop, NLevel, PLevel, KLevel, PhLevel).


/* =========================================================
   SECTION 4: Numeric Input → Recommendation
   =========================================================
   recommend_from_values(+N, +P, +K, +Ph, -Crop)
   Classifies raw numeric values then queries the rules.
   ========================================================= */

recommend_from_values(N, P, K, Ph, Crop) :-
    nitrogen_level(N, NLevel),
    phosphorus_level(P, PLevel),
    potassium_level(K, KLevel),
    ph_level(Ph, PhLevel),
    recommend_crop(NLevel, PLevel, KLevel, PhLevel, Crop).


/* =========================================================
   SECTION 5: Helper Queries
   ========================================================= */

% What soil type is suitable for a given crop?
suitable_soil(Crop, soil(NLevel, PLevel, KLevel, PhLevel)) :-
    crop_needs(Crop, NLevel, PLevel, KLevel, PhLevel).

% What pH does a crop prefer?
best_ph(Crop, PhLevel) :-
    crop_needs(Crop, _, _, _, PhLevel).

% List all crops that thrive in acidic soil
acid_tolerant(Crop) :-
    crop_needs(Crop, _, _, _, acidic).

% List all crops that thrive in alkaline soil
alkali_tolerant(Crop) :-
    crop_needs(Crop, _, _, _, alkaline) ;
    crop_needs(Crop, _, _, _, slightly_alkaline).

% List high-nitrogen crops
nitrogen_hungry(Crop) :-
    crop_needs(Crop, high, _, _, _).


/* =========================================================
   SECTION 6: Sample Interactive Session
   =========================================================

   After loading in SWI-Prolog, try:

   1. Recommend a crop from symbolic levels:
      ?- recommend_crop(high, medium, medium, slightly_acidic, Crop).

   2. Recommend from raw numeric values:
      ?- recommend_from_values(90, 42, 43, 6.0, Crop).

   3. What soil does rice need?
      ?- suitable_soil(rice, Soil).

   4. What pH does coffee prefer?
      ?- best_ph(coffee, Ph).

   5. Which crops tolerate acidic soil?
      ?- acid_tolerant(Crop).

   6. Which crops need lots of nitrogen?
      ?- nitrogen_hungry(Crop).

   7- Which crop fits N=90, P=42, K=43, pH=6.2 exactly?
      ?- recommend_from_values(90, 42, 43, 6.2, Crop).

   ========================================================= */
