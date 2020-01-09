
/* Generated data (by glib-mkenums) */

#include <config.h>

#include "ev-view-type-builtins.h"

/* enumerations from "ev-jobs.h" */
#include "ev-jobs.h"
GType
ev_job_run_mode_get_type (void)
{
  static volatile gsize g_define_type_id__volatile = 0;
 
  if (g_once_init_enter (&g_define_type_id__volatile)) {
    static const GEnumValue values[] = {
      { EV_JOB_RUN_THREAD, "EV_JOB_RUN_THREAD", "thread" },
      { EV_JOB_RUN_MAIN_LOOP, "EV_JOB_RUN_MAIN_LOOP", "main-loop" },
      { 0, NULL, NULL }
    };
    GType g_define_type_id = \
       g_enum_register_static (g_intern_static_string ("EvJobRunMode"), values);
      
    g_once_init_leave (&g_define_type_id__volatile, g_define_type_id);
  }
    
  return g_define_type_id__volatile;
}

GType
ev_render_flags_get_type (void)
{
  static volatile gsize g_define_type_id__volatile = 0;
 
  if (g_once_init_enter (&g_define_type_id__volatile)) {
    static const GFlagsValue values[] = {
      { EV_RENDER_INCLUDE_NONE, "EV_RENDER_INCLUDE_NONE", "none" },
      { EV_RENDER_INCLUDE_LINKS, "EV_RENDER_INCLUDE_LINKS", "links" },
      { EV_RENDER_INCLUDE_TEXT, "EV_RENDER_INCLUDE_TEXT", "text" },
      { EV_RENDER_INCLUDE_SELECTION, "EV_RENDER_INCLUDE_SELECTION", "selection" },
      { EV_RENDER_INCLUDE_IMAGES, "EV_RENDER_INCLUDE_IMAGES", "images" },
      { EV_RENDER_INCLUDE_FORMS, "EV_RENDER_INCLUDE_FORMS", "forms" },
      { EV_RENDER_INCLUDE_ANNOTS, "EV_RENDER_INCLUDE_ANNOTS", "annots" },
      { EV_RENDER_INCLUDE_ALL, "EV_RENDER_INCLUDE_ALL", "all" },
      { 0, NULL, NULL }
    };
    GType g_define_type_id = \
       g_flags_register_static (g_intern_static_string ("EvRenderFlags"), values);
      
    g_once_init_leave (&g_define_type_id__volatile, g_define_type_id);
  }
    
  return g_define_type_id__volatile;
}

/* enumerations from "ev-job-scheduler.h" */
#include "ev-job-scheduler.h"
GType
ev_job_priority_get_type (void)
{
  static volatile gsize g_define_type_id__volatile = 0;
 
  if (g_once_init_enter (&g_define_type_id__volatile)) {
    static const GEnumValue values[] = {
      { EV_JOB_PRIORITY_URGENT, "EV_JOB_PRIORITY_URGENT", "priority-urgent" },
      { EV_JOB_PRIORITY_HIGH, "EV_JOB_PRIORITY_HIGH", "priority-high" },
      { EV_JOB_PRIORITY_LOW, "EV_JOB_PRIORITY_LOW", "priority-low" },
      { EV_JOB_PRIORITY_NONE, "EV_JOB_PRIORITY_NONE", "priority-none" },
      { EV_JOB_N_PRIORITIES, "EV_JOB_N_PRIORITIES", "n-priorities" },
      { 0, NULL, NULL }
    };
    GType g_define_type_id = \
       g_enum_register_static (g_intern_static_string ("EvJobPriority"), values);
      
    g_once_init_leave (&g_define_type_id__volatile, g_define_type_id);
  }
    
  return g_define_type_id__volatile;
}

/* enumerations from "ev-view.h" */
#include "ev-view.h"
GType
ev_sizing_mode_get_type (void)
{
  static volatile gsize g_define_type_id__volatile = 0;
 
  if (g_once_init_enter (&g_define_type_id__volatile)) {
    static const GEnumValue values[] = {
      { EV_SIZING_BEST_FIT, "EV_SIZING_BEST_FIT", "best-fit" },
      { EV_SIZING_FIT_WIDTH, "EV_SIZING_FIT_WIDTH", "fit-width" },
      { EV_SIZING_FREE, "EV_SIZING_FREE", "free" },
      { 0, NULL, NULL }
    };
    GType g_define_type_id = \
       g_enum_register_static (g_intern_static_string ("EvSizingMode"), values);
      
    g_once_init_leave (&g_define_type_id__volatile, g_define_type_id);
  }
    
  return g_define_type_id__volatile;
}

GType
ev_view_selection_mode_get_type (void)
{
  static volatile gsize g_define_type_id__volatile = 0;
 
  if (g_once_init_enter (&g_define_type_id__volatile)) {
    static const GEnumValue values[] = {
      { EV_VIEW_SELECTION_TEXT, "EV_VIEW_SELECTION_TEXT", "text" },
      { EV_VIEW_SELECTION_RECTANGLE, "EV_VIEW_SELECTION_RECTANGLE", "rectangle" },
      { 0, NULL, NULL }
    };
    GType g_define_type_id = \
       g_enum_register_static (g_intern_static_string ("EvViewSelectionMode"), values);
      
    g_once_init_leave (&g_define_type_id__volatile, g_define_type_id);
  }
    
  return g_define_type_id__volatile;
}



/* Generated data ends here */

