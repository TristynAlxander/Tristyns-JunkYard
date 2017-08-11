package me.tristyn.pointsofinterest;

import android.app.Activity;
import android.content.res.Resources;       // Used to get Image Dimensions
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Point;
import android.graphics.drawable.BitmapDrawable;
import android.support.design.widget.FloatingActionButton;
import android.text.Layout;
import android.view.Display;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.RelativeLayout;

public final class ImgLoader {
    
    // Private Non-Instantiable Constructor.
    private ImgLoader(){}
    
    public class ImageButtonLoader {
        
    }
    
    // # Load Icon.
    // Methods
    //    loadIcon(getResources(), myButton, R.id.myHeight, R.id.myWidth, R.id.myDrawable)
    //    loadIcon(getResources(), myButton, R.id.myHeight, R.id.myWidth, myPath)
    // Variables
    //    myButton ImageButton or FloatingActionButton the image is to be assigned to.
    //      myButton = (ImageButton) findViewById(R.id.myImageButton);
    //        where myImageButton is from <ImageButton android:id            = "@+id/myImageButton" ... />
    //      myButton = (FloatingActionButton) findViewById(R.id.myFloatingActionButton);
    //        where myFloatingActionButton is from <ImageButton android:id            = "@+id/myFloatingActionButton" ... />
    //    myHeight      from <ImageButton android:layout_height = "@dimen/myHeight"    ... />
    //    myWidth       from <ImageButton android:layout_width  = "@dimen/myWidth"     ... />
    //    myDrawable    from app/res/drawable/
    //    myPath        from File Path to a drawable.
    
    public static void loadImage(Resources resource, ImageButton button, int imageButtonWidth, int imageButtonHeight, int drawableID) {
        
        // Converts dimension to pixels.                                                            // Converts dimension to pixels.
        int heightPixels = (int) resource.getDimension(imageButtonHeight);
        int widthPixels = (int) resource.getDimension(imageButtonWidth);
        
        // Get & Set Bitmap                                                                         // Get & Set Bitmap
        Bitmap imageBitmap = getDecodedBitmap(resource, drawableID, widthPixels, heightPixels);
        button.setImageBitmap(imageBitmap);
        }
    
    public static void loadImage(Resources resource, ImageButton button, int imageButtonWidth, int imageButtonHeight, String drawablePath) {
    
        // Converts dimension to pixels.                                                            // Converts dimension to pixels.
        int heightPixels = (int) resource.getDimension(imageButtonHeight);
        int widthPixels = (int) resource.getDimension(imageButtonWidth);
    
        // Get & Set Bitmap                                                                         // Get & Set Bitmap
        Bitmap imageBitmap = getDecodedBitmap(drawablePath, widthPixels, heightPixels);
        button.setImageBitmap(imageBitmap);
        }
    
    public static void loadImage(Resources resource, FloatingActionButton button, int imageButtonWidth, int imageButtonHeight, int drawableID) {
        
        // Converts dimension to pixels.                                                            // Converts dimension to pixels.
        int heightPixels = (int) resource.getDimension(imageButtonHeight);
        int widthPixels = (int) resource.getDimension(imageButtonWidth);
        
        // Get & Set Bitmap                                                                         // Get & Set Bitmap
        Bitmap imageBitmap = getDecodedBitmap(resource, drawableID, widthPixels, heightPixels);
        button.setImageBitmap(imageBitmap);
        }
    
    public static void loadImage(Resources resource, FloatingActionButton button, int imageButtonWidth, int imageButtonHeight, String drawablePath) {
    
        // Converts dimension to pixels.                                                            // Converts dimension to pixels.
        int heightPixels = (int) resource.getDimension(imageButtonHeight);
        int widthPixels = (int) resource.getDimension(imageButtonWidth);
    
        // Get & Set Bitmap                                                                         // Get & Set Bitmap
        Bitmap imageBitmap = getDecodedBitmap(drawablePath, widthPixels, heightPixels);
        button.setImageBitmap(imageBitmap);
        }
    
    public static void loadActivityBg(Activity activity, ImageView view, int drawableID){
        // Get dimensions in pixels.
        Display display = activity.getWindowManager().getDefaultDisplay();
        Point size = new Point();
        display.getSize(size);
        int widthPixels = size.x;
        int heightPixels = size.y;
        
        // Get & Set Bitmap                                                                         // Get & Set Bitmap
        Resources resource = activity.getResources();
        Bitmap imageBitmap = getDecodedBitmap(resource, drawableID, widthPixels, heightPixels);
        view.setImageBitmap(imageBitmap);
        view.setScaleType(ImageView.ScaleType.CENTER_CROP);
        }
        
    
    
    // # Get Decoded Bitmap
    // Methods
    //    getDecodedBitmap(resource, drawableID, widthPixels, heightPixels)
    //    getDecodedBitmap(drawablePath, widthPixels, heightPixels);
    // Variables
    //    resource      Activity Resource used to get drawable
    //    drawableID    Drawable ID R.id.myDrawable from app/res/drawable/
    //    drawablePath  File Path to a drawable.
    //    widthPixels   ImageButton's Width  in Pixels
    //    heightPixels  ImageButton's Height in Pixels
    
    private static Bitmap getDecodedBitmap(Resources resource, int drawableID, int widthPixels, int heightPixels){
        
        // Decode bounds.
        final BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeResource(resource, drawableID, options);
        
        // Get Sample Size.
        options.inSampleSize = getSampleSize(options, widthPixels, heightPixels);
    
        // Decode whole bitmap.
        options.inJustDecodeBounds = false;
        return BitmapFactory.decodeResource(resource, drawableID, options);
        }
    
    private static Bitmap getDecodedBitmap(String drawablePath, int widthPixels, int heightPixels){
        
        // Decode bounds
        final BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeFile(drawablePath, options);
    
        // Get Sample Size.
        options.inSampleSize = getSampleSize(options, widthPixels, heightPixels);
        
        // Decode whole bitmap.
        options.inJustDecodeBounds = false;
        return BitmapFactory.decodeFile(drawablePath, options);
        }
    
    
    // # Sample Size
    // Sample Size is the pixels sampled per pixel decoded.
    // It always grows as 2^n because bitmaps are square.
    
    private static int getSampleSize(BitmapFactory.Options options, int buttonWidthPixles, int buttonHeightPixles) {
        
        // Get Bitmap's Raw Dimensions
        final int rawBitmapHeight = options.outHeight;
        final int rawBitmapWidth = options.outWidth;
        
        // Default 1:1 sample size.
        int inSampleSize = 1;
        
        
        // If either raw dimension if greater than necessary
        if (rawBitmapWidth > buttonWidthPixles || rawBitmapHeight > buttonHeightPixles) {
            
            // Get Half Dimensions
            final int halfHeight = rawBitmapHeight / 2;
            final int halfWidth = rawBitmapWidth / 2;
            
            // Double sample size while both sides still in excess
            while (    (halfHeight / inSampleSize) >= buttonHeightPixles
                    && (halfWidth  / inSampleSize) >= buttonWidthPixles ){inSampleSize *= 2;}
            
            }
        return inSampleSize;
        }
    
    
    }
