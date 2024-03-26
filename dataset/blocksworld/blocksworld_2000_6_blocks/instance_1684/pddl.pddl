

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c a)
(ontable d)
(ontable e)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on d b))
)
)


