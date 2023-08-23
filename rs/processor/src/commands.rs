use serde_json::{Map, Value, json};

use crate::process_task;

pub async fn process_chart_arguments(arguments: Vec<&str>, platforms: Vec<&str>, ticker_id: Option<&str>, defaults: Map<String, Value>) -> (Option<Value>, Option<Value>) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": ticker_id,
			"defaults": defaults
		}),
		"parser",
		Some("/chart"),
		None,
		None
	).await;

	if let Err(e) = payload {
		(None, Some(json!({"error": e.to_string()})))
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(Some(payload.get("message").unwrap().clone()), Some(payload.get("response").unwrap().clone()))
	}
}

pub async fn process_heatmap_arguments(arguments: Vec<&str>, platforms: Vec<&str>) -> (Option<Value>, Option<Value>) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms
		}),
		"parser",
		Some("/heatmap"),
		None,
		None
	).await;

	if let Err(e) = payload {
		(None, Some(json!({"error": e.to_string()})))
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(Some(payload.get("message").unwrap().clone()), Some(payload.get("response").unwrap().clone()))
	}
}

pub async fn process_quote_arguments(arguments: Vec<&str>, platforms: Vec<&str>, ticker_id: Option<&str>) -> (Option<Value>, Option<Value>) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": ticker_id
		}),
		"parser",
		Some("/quote"),
		None,
		None
	).await;

	if let Err(e) = payload {
		(None, Some(json!({"error": e.to_string()})))
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(Some(payload.get("message").unwrap().clone()), Some(payload.get("response").unwrap().clone()))
	}
}

pub async fn process_detail_arguments(arguments: Vec<&str>, platforms: Vec<&str>, ticker_id: Option<&str>) -> (Option<Value>, Option<Value>) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": ticker_id
		}),
		"parser",
		Some("/detail"),
		None,
		None
	).await;

	if let Err(e) = payload {
		(None, Some(json!({"error": e.to_string()})))
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(Some(payload.get("message").unwrap().clone()), Some(payload.get("response").unwrap().clone()))
	}
}