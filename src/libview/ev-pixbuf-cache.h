/* this file is part of evince, a gnome document viewer
 *
 *  Copyright (C) 2005 Red Hat, Inc
 *
 * Evince is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Evince is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */

/* This File is basically an extention of EvView, and is out here just to keep
 * ev-view.c from exploding.
 */

#if !defined (__EV_EVINCE_VIEW_H_INSIDE__) && !defined (EVINCE_COMPILATION)
#error "Only <evince-view.h> can be included directly."
#endif

#ifndef __EV_PIXBUF_CACHE_H__
#define __EV_PIXBUF_CACHE_H__

#include <gtk/gtk.h>

#include <evince-document.h>

G_BEGIN_DECLS

#define EV_TYPE_PIXBUF_CACHE            (ev_pixbuf_cache_get_type ())
#define EV_PIXBUF_CACHE(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), EV_TYPE_PIXBUF_CACHE, EvPixbufCache))
#define EV_IS_PIXBUF_CACHE(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), EV_TYPE_PIXBUF_CACHE))



/* The coordinates in the rect here are at scale == 1.0, so that we can ignore
 * resizings.  There is one per page, maximum.
 */
typedef struct {
	int page;
	EvRectangle rect;
	GdkRegion *covered_region;
	EvSelectionStyle style;
} EvViewSelection;

typedef struct _EvPixbufCache       EvPixbufCache;
typedef struct _EvPixbufCacheClass  EvPixbufCacheClass;

GType          ev_pixbuf_cache_get_type             (void) G_GNUC_CONST;
EvPixbufCache *ev_pixbuf_cache_new                  (GtkWidget     *view,
						     EvDocument    *document);
void           ev_pixbuf_cache_set_page_range       (EvPixbufCache *pixbuf_cache,
						     gint           start_page,
						     gint           end_page,
						     gint	    rotation,
						     gfloat         scale,
						     GList          *selection_list);
cairo_surface_t *ev_pixbuf_cache_get_surface        (EvPixbufCache *pixbuf_cache,
						     gint           page);
GList         *ev_pixbuf_cache_get_link_mapping     (EvPixbufCache *pixbuf_cache,
						     gint           page);
GList         *ev_pixbuf_cache_get_image_mapping    (EvPixbufCache *pixbuf_cache,
						     gint           page);
GdkRegion     *ev_pixbuf_cache_get_text_mapping     (EvPixbufCache *pixbuf_cache,
						     gint           page);
GList 	      *ev_pixbuf_cache_get_form_field_mapping (EvPixbufCache *pixbuf_cache,
						       gint 	    page);
GList         *ev_pixbuf_cache_get_annots_mapping   (EvPixbufCache *pixbuf_cache,
						     gint           page);
void           ev_pixbuf_cache_clear                (EvPixbufCache *pixbuf_cache);
void           ev_pixbuf_cache_style_changed        (EvPixbufCache *pixbuf_cache);
void           ev_pixbuf_cache_reload_page 	    (EvPixbufCache *pixbuf_cache,
						     GdkRegion     *region,
                    				     gint           page,
			                             gint           rotation,
                         			     gdouble         scale);
/* Selection */
cairo_surface_t *ev_pixbuf_cache_get_selection_surface (EvPixbufCache *pixbuf_cache,
							gint           page,
							gfloat         scale,
							GdkRegion     **region);
void           ev_pixbuf_cache_set_selection_list   (EvPixbufCache *pixbuf_cache,
						     GList         *selection_list);
GList         *ev_pixbuf_cache_get_selection_list   (EvPixbufCache *pixbuf_cache);

G_END_DECLS

#endif /* __EV_PIXBUF_CACHE_H__ */
