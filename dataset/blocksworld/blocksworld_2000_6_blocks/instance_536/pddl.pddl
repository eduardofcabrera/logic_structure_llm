

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(on d c)
(ontable e)
(clear a)
(clear b)
(clear e)
)
(:goal
(and
(on a b)
(on b d)
(on d c))
)
)


