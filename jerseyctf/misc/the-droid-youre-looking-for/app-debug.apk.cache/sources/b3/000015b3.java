package kotlinx.coroutines;

import androidx.constraintlayout.widget.ConstraintLayout;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicInteger;
import kotlin.Metadata;

/* compiled from: ThreadPoolDispatcher.kt */
@Metadata(d1 = {"\u0000\u0016\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\b\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\u001a\u0018\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H\u0007\u001a\u0010\u0010\u0006\u001a\u00020\u00012\u0006\u0010\u0004\u001a\u00020\u0005H\u0007¨\u0006\u0007"}, d2 = {"newFixedThreadPoolContext", "Lkotlinx/coroutines/ExecutorCoroutineDispatcher;", "nThreads", "", "name", "", "newSingleThreadContext", "kotlinx-coroutines-core"}, k = 2, mv = {1, 6, 0}, xi = ConstraintLayout.LayoutParams.Table.LAYOUT_CONSTRAINT_VERTICAL_CHAINSTYLE)
/* loaded from: classes.dex */
public final class ThreadPoolDispatcherKt {
    /* renamed from: $r8$lambda$IYX-93i18CF3E6e1K_suGGxRFcI */
    public static /* synthetic */ Thread m1578$r8$lambda$IYX93i18CF3E6e1K_suGGxRFcI(int i, String str, AtomicInteger atomicInteger, Runnable runnable) {
        return m1579newFixedThreadPoolContext$lambda1(i, str, atomicInteger, runnable);
    }

    public static final ExecutorCoroutineDispatcher newSingleThreadContext(String name) {
        return newFixedThreadPoolContext(1, name);
    }

    public static final ExecutorCoroutineDispatcher newFixedThreadPoolContext(final int nThreads, final String name) {
        if (!(nThreads >= 1)) {
            throw new IllegalArgumentException(("Expected at least one thread, but " + nThreads + " specified").toString());
        }
        final AtomicInteger threadNo = new AtomicInteger();
        ScheduledExecutorService executor = Executors.newScheduledThreadPool(nThreads, new ThreadFactory() { // from class: kotlinx.coroutines.ThreadPoolDispatcherKt$$ExternalSyntheticLambda0
            @Override // java.util.concurrent.ThreadFactory
            public final Thread newThread(Runnable runnable) {
                return ThreadPoolDispatcherKt.m1578$r8$lambda$IYX93i18CF3E6e1K_suGGxRFcI(nThreads, name, threadNo, runnable);
            }
        });
        return ExecutorsKt.from((ExecutorService) executor);
    }

    /* renamed from: newFixedThreadPoolContext$lambda-1 */
    public static final Thread m1579newFixedThreadPoolContext$lambda1(int $nThreads, String $name, AtomicInteger $threadNo, Runnable runnable) {
        Thread t = new Thread(runnable, $nThreads == 1 ? $name : $name + '-' + $threadNo.incrementAndGet());
        t.setDaemon(true);
        return t;
    }
}