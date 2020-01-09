/* ev-document-layers.c
 *  this file is part of evince, a gnome document_links viewer
 * 
 * Copyright (C) 2008 Carlos Garcia Campos  <carlosgc@gnome.org>
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

#include "config.h"

#include "ev-document-layers.h"
#include "ev-document.h"

EV_DEFINE_INTERFACE (EvDocumentLayers, ev_document_layers, 0)

static void
ev_document_layers_class_init (EvDocumentLayersIface *klass)
{
}

gboolean
ev_document_layers_has_layers (EvDocumentLayers *document_layers)
{
	EvDocumentLayersIface *iface = EV_DOCUMENT_LAYERS_GET_IFACE (document_layers);

	return iface->has_layers (document_layers);
}

GtkTreeModel *
ev_document_layers_get_layers (EvDocumentLayers *document_layers)
{
	EvDocumentLayersIface *iface = EV_DOCUMENT_LAYERS_GET_IFACE (document_layers);

	return iface->get_layers (document_layers);
}

void
ev_document_layers_show_layer (EvDocumentLayers *document_layers,
			       EvLayer          *layer)
{
	EvDocumentLayersIface *iface = EV_DOCUMENT_LAYERS_GET_IFACE (document_layers);

	iface->show_layer (document_layers, layer);
}

void
ev_document_layers_hide_layer (EvDocumentLayers *document_layers,
			       EvLayer          *layer)
{
	EvDocumentLayersIface *iface = EV_DOCUMENT_LAYERS_GET_IFACE (document_layers);

	iface->hide_layer (document_layers, layer);
}

gboolean
ev_document_layers_layer_is_visible (EvDocumentLayers *document_layers,
				     EvLayer          *layer)
{
	EvDocumentLayersIface *iface = EV_DOCUMENT_LAYERS_GET_IFACE (document_layers);

	return iface->layer_is_visible (document_layers, layer);
}
