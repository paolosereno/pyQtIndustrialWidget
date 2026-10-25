#ifndef BINDINGS_H
#define BINDINGS_H

#ifndef QT_ANNOTATE_ACCESS_SPECIFIER
#define QT_ANNOTATE_ACCESS_SPECIFIER(a)
#endif

// 12 widget headers of QtIndustrialWidgets
#if defined(__has_include)
  #if __has_include(<QtIndustrialWidgets/RadialGauge.h>)
    #include <QtIndustrialWidgets/RadialGauge.h>
    #include <QtIndustrialWidgets/LinearGauge.h>
    #include <QtIndustrialWidgets/IndustrialKnob.h>
    #include <QtIndustrialWidgets/SevenSegmentDisplay.h>
    #include <QtIndustrialWidgets/LedIndicator.h>
    #include <QtIndustrialWidgets/StripChart.h>
    #include <QtIndustrialWidgets/IndustrialSwitch.h>
    #include <QtIndustrialWidgets/LevelMeter.h>
    #include <QtIndustrialWidgets/AnnunciatorPanel.h>
    #include <QtIndustrialWidgets/Compass.h>
    #include <QtIndustrialWidgets/CircularBargraph.h>
    #include <QtIndustrialWidgets/AnalysisChart.h>
  #else
    #include "radialgauge.h"
    #include "lineargauge.h"
    #include "industrialknob.h"
    #include "sevensegmentdisplay.h"
    #include "ledindicator.h"
    #include "stripchart.h"
    #include "industrialswitch.h"
    #include "levelmeter.h"
    #include "annunciatorpanel.h"
    #include "compass.h"
    #include "circularbargraph.h"
    #include "analysischart.h"
  #endif
#else
  #include <QtIndustrialWidgets/RadialGauge.h>
  #include <QtIndustrialWidgets/LinearGauge.h>
  #include <QtIndustrialWidgets/IndustrialKnob.h>
  #include <QtIndustrialWidgets/SevenSegmentDisplay.h>
  #include <QtIndustrialWidgets/LedIndicator.h>
  #include <QtIndustrialWidgets/StripChart.h>
  #include <QtIndustrialWidgets/IndustrialSwitch.h>
  #include <QtIndustrialWidgets/LevelMeter.h>
  #include <QtIndustrialWidgets/AnnunciatorPanel.h>
  #include <QtIndustrialWidgets/Compass.h>
  #include <QtIndustrialWidgets/CircularBargraph.h>
  #include <QtIndustrialWidgets/AnalysisChart.h>
#endif

#endif // BINDINGS_H
