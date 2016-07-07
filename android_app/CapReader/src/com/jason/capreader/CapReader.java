package com.jason.capreader;

import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.components.Legend.LegendForm;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.components.YAxis.AxisDependency;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.interfaces.datasets.IDataSet;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.TextView;

public class CapReader extends Activity
{

	private Button m_btnStart;
	private TextView m_tvOutput;
	private CheckBox m_cbSave2File;
	private LineChart m_chart;

	private boolean m_bSave2File = false;
	private boolean m_bRunning = false;
	private Thread m_dataThread = null;
	private Queue<Integer> m_queue = null;
	public Handler m_uiHandler = new Handler()
	{
		@Override
		public void handleMessage(Message msg)
		{
			if (msg.what == Common.HMSG_NEW_DATA)
			{
				Bundle b = msg.getData();
				int nVal = b.getInt(Common.DATA_KEY);

				// update lineDataSet
				LineData data = m_chart.getData();
				LineDataSet ds = (LineDataSet) data.getDataSetByIndex(0);
				data.addXValue("");
				data.addEntry(new Entry(nVal, ds.getEntryCount() ), 0);
				
				// clear old data if it's full
				if(ds.getEntryCount() == Common.MAX_DATA_SIZE)
				{
					data.removeXValue(0);
					ds.removeEntry(0);
					
					for (Entry entry : ds.getYVals() ) {
		                entry.setXIndex(entry.getXIndex() - 1);
		            }
				}

				
				// notify
				data.notifyDataChanged();
				m_chart.notifyDataSetChanged();
				m_chart.invalidate();
			}
		}
	};

	public CapReader()
	{
		m_queue = new ConcurrentLinkedQueue<Integer>();
	}

	@Override
	protected void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_cap_reader);

		// connect to resource
		m_btnStart = (Button) findViewById(R.id.button_start);
		m_tvOutput = (TextView) findViewById(R.id.textView_output);
		m_cbSave2File = (CheckBox) findViewById(R.id.checkBox_save2File);
		m_chart = (LineChart) findViewById(R.id.chart);

		initializeChart(m_chart);
		
	}

	private void initializeChart(LineChart chart)
	{
		// customize behavior
		chart.setDragEnabled(false);
		chart.setScaleEnabled(false);
		chart.setDrawGridBackground(true);
		chart.setBackgroundColor(Color.LTGRAY);
		chart.setDescription(" ");
		chart.setTouchEnabled(true);
		chart.setPinchZoom(true);
		chart.setScaleEnabled(true);
		chart.setDoubleTapToZoomEnabled(true);

		// set data
		LineData data = new LineData();
		LineDataSet ds = new LineDataSet(null, "capacitance");
		ds.setAxisDependency(AxisDependency.LEFT);
		ds.setDrawCircles(false);
		ds.setColor(Color.RED);
		data.addDataSet(ds);
		data.setDrawValues(false);
		m_chart.setData(data);

		// set legend
		Legend leg = chart.getLegend();
		leg.setForm(LegendForm.LINE);
		leg.setTextColor(Color.BLACK);

		// set X, Y axis
		XAxis xl = chart.getXAxis();
		xl.setTextColor(Color.BLACK);
		xl.setDrawGridLines(false);
		xl.setAvoidFirstLastClipping(true);

		YAxis yl = chart.getAxisLeft();
		yl.setTextColor(Color.BLACK);
		yl.setDrawGridLines(true);
		yl.setAxisMaxValue(1300f);
		yl.setAxisMinValue(0f);
		YAxis yl2 = chart.getAxisRight();
		yl2.setEnabled(false);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu)
	{
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.cap_reader, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item)
	{
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings)
		{
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	public void onBtnClicked_start(View btn)
	{
		m_bRunning = !m_bRunning;
		m_btnStart.setText(m_bRunning ? "stop" : "start");
		m_cbSave2File.setEnabled(!m_bRunning);

		if (m_bRunning)
		{
			output2log(String.format("Test is started."));

			m_dataThread = new Thread(
					new DataReader(Common.DEFAULT_INPUT_FILE_PATH, m_queue, m_uiHandler, m_bSave2File));
			m_dataThread.start();
		}
		else
		{
			try
			{
				m_dataThread.interrupt();
				m_dataThread.join();
				m_dataThread = null;
			}
			catch (InterruptedException e)
			{
				e.printStackTrace();
			}
		}

	}

	public void onSaveFile(View cb)
	{
		m_bSave2File = m_cbSave2File.isChecked();
	}

	private void output2log(String strTrace)
	{
		Log.i(Common.LOG_TAG, strTrace);
		m_tvOutput.setText(strTrace);
	}

}
