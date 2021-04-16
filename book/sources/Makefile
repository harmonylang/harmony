.SUFFIXES: .hny .tex

CODEDIR = ../../code

%.tex: $(CODEDIR)/%.hny
	python3 pp.py $< > $@

CODE = \
    BBhoare.tex \
    BBsema.tex \
    BBsemadata.tex \
    BBsematest.tex \
    Diners.tex \
    DinersAvoid.tex \
    DinersCV.tex \
    DinersSema.tex \
    Peterson.tex \
    PetersonInductive.tex \
    PetersonMethod.tex \
    RW.tex \
    RWbusychk.tex \
    RWcv.tex \
    RWfair.tex \
    RWlock.tex \
    RWmulti.tex \
    RWqtest.tex \
    RWqueue.tex \
    RWsbs.tex \
    RWtest.tex \
    Up.tex \
    UpEnter.tex \
    UpLock.tex \
    abp.tex \
    abptest.tex \
    actor.tex \
    actortest.tex \
    atm.tex \
    atomicinc.tex \
    baddblwait.tex \
    bank.tex \
    barrier.tex \
    barrier1.tex \
    barriertest.tex \
    clock.tex \
    counter.tex \
    cs.tex \
    cslock.tex \
    csTAS.tex \
    csbarebones.tex \
    csonebit.tex \
    dinersfix.tex \
    dinersfix2.tex \
    gpu.tex \
    hoare.tex \
    hw.tex \
    linkedlist.tex \
    lltest.tex \
    lockintf.tex \
    locksusp.tex \
    mesa.tex \
    multitest.tex \
    naiveFlags.tex \
    naiveLock.tex \
    naiveTurn.tex \
    oo.tex \
    prog1.tex \
    prog2.tex \
    qbarrier.tex \
    queue.tex \
    queuedemo.tex \
    queuelin.tex \
    queueMS.tex \
    queuespec.tex \
    qtestseq.tex \
    qtestconc.tex \
    qtest1.tex \
    qtest2.tex \
    qtest3.tex \
    qtest4.tex \
    qsort.tex \
    qsorttest.tex \
    spinlock.tex \
    spinlockInv.tex \
    stacktest.tex \
    stack1.tex \
    stack2.tex \
    stack3.tex \
    stack4.tex \
    trap.tex \
    trap2.tex \
    trap3.tex \
    trap4.tex \
    trap5.tex \
    trap6.tex \
    triangle.tex \
    xy.tex

all: $(CODE)
